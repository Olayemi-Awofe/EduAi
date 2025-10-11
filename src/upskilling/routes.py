from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.core.security import get_current_teacher
from . import models, schemas
from utils import generate_skill
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime
from src.dashboard.models import TeacherMonthlyAnalytics

router = APIRouter(prefix="/upskilling", tags=["Upskilling"])
class SectionProgressUpdate(BaseModel):
    skill_id: int
    section_id: int

def get_current_month_str():
    # e.g., "Oct-2025"
    return datetime.utcnow().strftime("%b-%Y")

# ===== Skills =====
@router.post("/skills", response_model=schemas.SkillOut)
def create_skill(
    skill: schemas.SkillCreate, 
    db: Session = Depends(get_db), 
    current_teacher=Depends(get_current_teacher)):

    title = skill.title
    level = skill.level

    response = generate_skill(title, level)

    skill_info = response.get("skill")
    sections = response.get("sections")
    test = response.get("test")
    questions = test.get("questions")

    if not skill_info or not sections or not test:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate skill information."
        )
    
    new_skill = models.Skill(
        teacher_id=current_teacher.id,
        title=skill_info["title"],
        description=skill_info.get("description"),
        level=level,
        total_sections=skill_info.get("total_sections", len(sections)),
        category=skill_info.get("category"),
        estimated_duration=skill_info.get("estimated_duration"),
        thumbnail_url=skill_info.get("thumbnail_url"),
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    #create teacher skill progress
    new_progress = models.TeacherSkillProgress(
        teacher_id=current_teacher.id,
        skill_id=new_skill.id,
        completed_sections=0,
        progress=0.0,
        completed=False,
        score=0,
    )

    db.add(new_progress)
    db.commit()

    #save sections in bulk
    section_objects = [
        models.Section(
        teacher_id=current_teacher.id,
        skill_id=new_skill.id,
        order=section.get("order"),
        title=section.get("title"),
        content=section.get("content"),
        video_url=section.get("video_url"),
        resource_url=section.get("resource_url"),
        duration=section.get("duration"),
        quiz_included=section.get("quiz_included", False),
        completed=False
    )
    for section in sections
    ]

    db.bulk_save_objects(section_objects)
    db.commit()


    #create test
    new_test = models.Test(
        teacher_id=current_teacher.id,
        skill_id=new_skill.id,
        status="generate",
        score=0,
        total_questions=test.get("total_questions"),
        time_limit=test.get("time_limit"),
        attempts=test.get("attempts")
    )

    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    #save questions in bulk
    question_objects  = [
        models.Question(
            teacher_id=current_teacher.id,
            skill_id=new_skill.id,
            test_id=new_test.id,
            question=item.get("question"),
            options=item.get("options"),
            correct_answer=item.get("correct_answer"),
            explanation=item.get("explanation"),
            difficulty=item.get("difficulty")
        )
        for item in questions
    ]

    db.bulk_save_objects(question_objects)
    db.commit()

    #analytics
    month_str = get_current_month_str()
    record = db.query(TeacherMonthlyAnalytics).filter_by(
        teacher_id=current_teacher.id,
        month=month_str
    ).first()
    if record:
        record.upskilling += 1
    else:
        record = TeacherMonthlyAnalytics(
            teacher_id=current_teacher.id,
            upskilling=1,
            month=month_str
        )
    db.add(record)
    db.commit()
    db.refresh(record)

    return new_skill


@router.get("/skills", response_model=list[schemas.SkillRead])
def get_skills(
    db: Session = Depends(get_db),
    current_teacher=Depends(get_current_teacher)
):
    skills = (
        db.query(models.Skill)
        .filter(models.Skill.teacher_id == current_teacher.id)
        .order_by(models.Skill.created_at.desc())
        .all()
    )

    # Eager load related data for each skill
    for skill in skills:
        skill.sections  # load sections
        skill.tests  # load tests
        # pick first test if only one test per skill
        skill.test = skill.tests[0] if skill.tests else None

        # Load teacher's progress for this skill (just one record)
        progress = (
            db.query(models.TeacherSkillProgress)
            .filter_by(skill_id=skill.id, teacher_id=current_teacher.id)
            .first()
        )
        skill.progress_record = progress

    return skills

@router.get("/skills/{skill_id}", response_model=schemas.SkillRead)
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_teacher=Depends(get_current_teacher)
):
    skill = (
        db.query(models.Skill)
        .filter(
            models.Skill.id == skill_id,
            models.Skill.teacher_id == current_teacher.id
        )
        .first()
    )

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Eager load related data
    skill.sections
    skill.tests
    for test in skill.tests:
        test.questions

    # Assign first test (if any)
    skill.test = skill.tests[0] if skill.tests else None

    # Get the teacher’s progress for this skill (just one)
    progress_record = (
        db.query(models.TeacherSkillProgress)
        .filter_by(skill_id=skill.id, teacher_id=current_teacher.id)
        .first()
    )
    skill.progress_record = progress_record  # attach single record

    return skill

@router.get("/progress/{skill_id}", response_model=schemas.TeacherSkillProgressOut)
def get_progress(skill_id: int, db: Session = Depends(get_db), current_teacher=Depends(get_current_teacher)):
    progress = (
        db.query(models.TeacherSkillProgress)
        .filter_by(skill_id=skill_id, teacher_id=current_teacher.id)
        .first()
    )
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return progress

@router.put("/progress/update", response_model=schemas.TeacherSkillProgressOut)
def update_section_progress(
   data: SectionProgressUpdate,
    db: Session = Depends(get_db),
    current_teacher=Depends(get_current_teacher)
):
    skill_id = data.skill_id
    section_id = data.section_id
    # Get the section
    section = db.query(models.Section).filter_by(id=section_id, skill_id=skill_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    # Mark section as completed
    if not section.completed:
        section.completed = True
        section.completed_at = datetime.utcnow()
        db.add(section)
        db.commit()

    # Get or create teacher progress
    progress = (
        db.query(models.TeacherSkillProgress)
        .filter_by(skill_id=skill_id, teacher_id=current_teacher.id)
        .first()
    )
    if not progress:
        raise HTTPException(status_code=404, detail="Teacher progress not found")

    #  Count total & completed sections
    total_sections = db.query(models.Section).filter_by(skill_id=skill_id).count()
    completed_sections = db.query(models.Section).filter_by(skill_id=skill_id, completed=True).count()

    # Update teacher progress
    progress.completed_sections = completed_sections
    progress.progress = int((completed_sections / total_sections) * 100)
    progress.completed = progress.progress == 100

    db.add(progress)
    db.commit()
    db.refresh(progress)

    #analytics
    month_str = get_current_month_str()
    record = db.query(TeacherMonthlyAnalytics).filter_by(
        teacher_id=current_teacher.id,
        month=month_str
    ).first()
    if record:
        record.upskilling += 1
    else:
        record = TeacherMonthlyAnalytics(
            teacher_id=current_teacher.id,
            upskilling=1,
            month=month_str
        )
    db.add(record)
    db.commit()
    db.refresh(record)

    return { "progress": int((completed_sections / total_sections) * 100) }


@router.post("/submit-test")
def submit_test(
    submission: schemas.TestSubmission,
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    # Fetch the test
    test = db.query(models.Test).filter(models.Test.skill_id == submission.skill_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found for this skill")

    correct_count = 0

    # Process each submitted answer
    for answer in submission.answers:
        question = db.query(models.Question).filter(models.Question.id == answer.id).first()
        if question:
            question.user_answer = answer.user_answer
            if question.user_answer.strip().lower() == question.correct_answer.strip().lower():
                question.correct = True
                correct_count += 1
            else:
                question.correct = False
            db.add(question)

    # Calculate score as a percentage
    total_questions = test.total_questions or len(submission.answers)
    score_percentage = round((correct_count / total_questions) * 100, 2)

    # Update test record
    test.status = "completed"
    test.score = score_percentage
    db.add(test)

    # Update teacher skill progress
    progress = db.query(models.TeacherSkillProgress).filter(
        models.TeacherSkillProgress.teacher_id == current_teacher.id,
        models.TeacherSkillProgress.skill_id == submission.skill_id
    ).first()

    if progress:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
        progress.progress = 100
        progress.score = score_percentage
        db.add(progress)

    db.commit()

     #analytics
    month_str = get_current_month_str()
    record = db.query(TeacherMonthlyAnalytics).filter_by(
        teacher_id=current_teacher.id,
        month=month_str
    ).first()
    if record:
        record.upskilling += 1
    else:
        record = TeacherMonthlyAnalytics(
            teacher_id=current_teacher.id,
            upskilling=1,
            month=month_str
        )
    db.add(record)
    db.commit()
    
    db.refresh(test)
    test.questions = db.query(models.Question).filter(models.Question.test_id == test.id).all()

    return {
        "message": "Test submitted successfully",
        "score": score_percentage,
        "total_questions": total_questions,
        "correct_answers": correct_count,
        "test": test
    }