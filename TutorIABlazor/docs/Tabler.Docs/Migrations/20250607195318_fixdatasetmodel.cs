using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Tabler.Docs.Migrations
{
    /// <inheritdoc />
    public partial class fixdatasetmodel : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_StudentSkills_StudentSubjects_StudentSubjectId",
                table: "StudentSkills");

            migrationBuilder.DropForeignKey(
                name: "FK_StudentSubjects_Users_UserId",
                table: "StudentSubjects");

            migrationBuilder.DropForeignKey(
                name: "FK_Subjects_SubjectSkills_SkillId",
                table: "Subjects");

            migrationBuilder.DropIndex(
                name: "IX_Subjects_SkillId",
                table: "Subjects");

            migrationBuilder.DropColumn(
                name: "SkillId",
                table: "Subjects");

            migrationBuilder.AddColumn<int>(
                name: "SubjectSkillDetailId",
                table: "SubjectStates",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<int>(
                name: "SubjectSkillId",
                table: "Subjects",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AlterColumn<int>(
                name: "UserId",
                table: "StudentSubjects",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AlterColumn<int>(
                name: "StudentSubjectId",
                table: "StudentSkills",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AlterColumn<string>(
                name: "Discriminator",
                table: "QuestionBases",
                type: "nvarchar(21)",
                maxLength: 21,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(34)",
                oldMaxLength: 34);

            migrationBuilder.CreateIndex(
                name: "IX_SubjectStates_SubjectSkillDetailId",
                table: "SubjectStates",
                column: "SubjectSkillDetailId");

            migrationBuilder.CreateIndex(
                name: "IX_Subjects_SubjectSkillId",
                table: "Subjects",
                column: "SubjectSkillId");

            migrationBuilder.AddForeignKey(
                name: "FK_StudentSkills_StudentSubjects_StudentSubjectId",
                table: "StudentSkills",
                column: "StudentSubjectId",
                principalTable: "StudentSubjects",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_StudentSubjects_Users_UserId",
                table: "StudentSubjects",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_Subjects_SubjectSkills_SubjectSkillId",
                table: "Subjects",
                column: "SubjectSkillId",
                principalTable: "SubjectSkills",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_SubjectStates_Subjects_SubjectSkillDetailId",
                table: "SubjectStates",
                column: "SubjectSkillDetailId",
                principalTable: "Subjects",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_StudentSkills_StudentSubjects_StudentSubjectId",
                table: "StudentSkills");

            migrationBuilder.DropForeignKey(
                name: "FK_StudentSubjects_Users_UserId",
                table: "StudentSubjects");

            migrationBuilder.DropForeignKey(
                name: "FK_Subjects_SubjectSkills_SubjectSkillId",
                table: "Subjects");

            migrationBuilder.DropForeignKey(
                name: "FK_SubjectStates_Subjects_SubjectSkillDetailId",
                table: "SubjectStates");

            migrationBuilder.DropIndex(
                name: "IX_SubjectStates_SubjectSkillDetailId",
                table: "SubjectStates");

            migrationBuilder.DropIndex(
                name: "IX_Subjects_SubjectSkillId",
                table: "Subjects");

            migrationBuilder.DropColumn(
                name: "SubjectSkillDetailId",
                table: "SubjectStates");

            migrationBuilder.DropColumn(
                name: "SubjectSkillId",
                table: "Subjects");

            migrationBuilder.AddColumn<int>(
                name: "SkillId",
                table: "Subjects",
                type: "int",
                nullable: true);

            migrationBuilder.AlterColumn<int>(
                name: "UserId",
                table: "StudentSubjects",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AlterColumn<int>(
                name: "StudentSubjectId",
                table: "StudentSkills",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AlterColumn<string>(
                name: "Discriminator",
                table: "QuestionBases",
                type: "nvarchar(34)",
                maxLength: 34,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(21)",
                oldMaxLength: 21);

            migrationBuilder.CreateIndex(
                name: "IX_Subjects_SkillId",
                table: "Subjects",
                column: "SkillId");

            migrationBuilder.AddForeignKey(
                name: "FK_StudentSkills_StudentSubjects_StudentSubjectId",
                table: "StudentSkills",
                column: "StudentSubjectId",
                principalTable: "StudentSubjects",
                principalColumn: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_StudentSubjects_Users_UserId",
                table: "StudentSubjects",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_Subjects_SubjectSkills_SkillId",
                table: "Subjects",
                column: "SkillId",
                principalTable: "SubjectSkills",
                principalColumn: "Id");
        }
    }
}
