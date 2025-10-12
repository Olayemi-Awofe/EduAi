CREATE TABLE "assessments"(
    "id" INTEGER NOT NULL,
    "lesson_id" INTEGER NOT NULL,
    "content" JSON NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "assessments" ADD PRIMARY KEY("id");
CREATE TABLE "curriculum_units"(
    "id" INTEGER NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "subject" VARCHAR(255) NOT NULL,
    "grade_level" VARCHAR(255) NOT NULL,
    "source_doc" TEXT NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "curriculum_units" ADD PRIMARY KEY("id");
CREATE TABLE "lessons"(
    "id" INTEGER NOT NULL,
    "curriculum_unit_id" INTEGER NOT NULL,
    "teacher_id" INTEGER NOT NULL,
    "topic" VARCHAR(255) NOT NULL,
    "subject" VARCHAR(255) NOT NULL,
    "grade" INTEGER NOT NULL,
    "duration" INTEGER NOT NULL,
    "content" JSON NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "lessons" ADD PRIMARY KEY("id");
CREATE TABLE "questions"(
    "id" INTEGER NOT NULL,
    "teacher_id" INTEGER NOT NULL,
    "skill_id" INTEGER NOT NULL,
    "test_id" INTEGER NOT NULL,
    "question" VARCHAR(255) NOT NULL,
    "question_type" VARCHAR(255) NOT NULL,
    "options" JSON NOT NULL,
    "correct_answer" VARCHAR(255) NOT NULL,
    "user_answer" VARCHAR(255) NOT NULL,
    "correct" BOOLEAN NOT NULL,
    "explanation" VARCHAR(255) NOT NULL,
    "difficulty" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "questions" ADD PRIMARY KEY("id");
CREATE TABLE "schools"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "region" VARCHAR(255) NOT NULL,
    "device_type" VARCHAR(255) NOT NULL,
    "connectivity" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "schools" ADD PRIMARY KEY("id");
CREATE TABLE "sections"(
    "id" INTEGER NOT NULL,
    "teacher_id" INTEGER NOT NULL,
    "skill_id" INTEGER NOT NULL,
    "order" INTEGER NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "content" VARCHAR(255) NOT NULL,
    "video_url" VARCHAR(255) NOT NULL,
    "resource_url" VARCHAR(255) NOT NULL,
    "duration" VARCHAR(255) NOT NULL,
    "quiz_included" BOOLEAN NOT NULL,
    "completed" BOOLEAN NOT NULL,
    "completed_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "sections" ADD PRIMARY KEY("id");
CREATE TABLE "skills"(
    "id" INTEGER NOT NULL,
    "teacher_id" INTEGER NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "level" INTEGER NOT NULL,
    "category" VARCHAR(255) NOT NULL,
    "total_sections" INTEGER NOT NULL,
    "estimated_duration" VARCHAR(255) NOT NULL,
    "thumbnail_url" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "skills" ADD PRIMARY KEY("id");
CREATE TABLE "teacher_monthly_analytics"(
    "id" INTEGER NOT NULL,
    "teacher_id" INTEGER NOT NULL,
    "lesson" INTEGER NOT NULL,
    "upskilling" INTEGER NOT NULL,
    "month" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "teacher_monthly_analytics" ADD PRIMARY KEY("id");
CREATE TABLE "teacher_skill_progress"(
    "id" INTEGER NOT NULL,
    "teacher_id" INTEGER NOT NULL,
    "skill_id" INTEGER NOT NULL,
    "completed_sections" INTEGER NOT NULL,
    "progress" DOUBLE PRECISION NOT NULL,
    "completed" BOOLEAN NOT NULL,
    "score" DOUBLE PRECISION NOT NULL,
    "started_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "completed_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "last_accessed_section_id" INTEGER NOT NULL
);
ALTER TABLE
    "teacher_skill_progress" ADD PRIMARY KEY("id");
CREATE TABLE "teachers"(
    "id" INTEGER NOT NULL,
    "name" INTEGER NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "phone" VARCHAR(255) NOT NULL,
    "school_id" INTEGER NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "teachers" ADD PRIMARY KEY("id");
CREATE TABLE "tests"(
    "id" INTEGER NOT NULL,
    "teacher_id" INTEGER NOT NULL,
    "skill_id" INTEGER NOT NULL,
    "status" VARCHAR(255) NOT NULL,
    "score" DOUBLE PRECISION NOT NULL,
    "total_questions" INTEGER NOT NULL,
    "time_limit" INTEGER NOT NULL,
    "attempts" INTEGER NOT NULL
);
ALTER TABLE
    "tests" ADD PRIMARY KEY("id");
ALTER TABLE
    "teacher_skill_progress" ADD CONSTRAINT "teacher_skill_progress_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id");
ALTER TABLE
    "lessons" ADD CONSTRAINT "lessons_curriculum_unit_id_foreign" FOREIGN KEY("curriculum_unit_id") REFERENCES "curriculum_units"("id");
ALTER TABLE
    "teacher_monthly_analytics" ADD CONSTRAINT "teacher_monthly_analytics_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id");
ALTER TABLE
    "assessments" ADD CONSTRAINT "assessments_lesson_id_foreign" FOREIGN KEY("lesson_id") REFERENCES "lessons"("id");
ALTER TABLE
    "lessons" ADD CONSTRAINT "lessons_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id");
ALTER TABLE
    "tests" ADD CONSTRAINT "tests_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id");
ALTER TABLE
    "questions" ADD CONSTRAINT "questions_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id");
ALTER TABLE
    "skills" ADD CONSTRAINT "skills_id_foreign" FOREIGN KEY("id") REFERENCES "skills"("id");
ALTER TABLE
    "skills" ADD CONSTRAINT "skills_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id");
ALTER TABLE
    "teachers" ADD CONSTRAINT "teachers_school_id_foreign" FOREIGN KEY("school_id") REFERENCES "schools"("id");
ALTER TABLE
    "sections" ADD CONSTRAINT "sections_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id");