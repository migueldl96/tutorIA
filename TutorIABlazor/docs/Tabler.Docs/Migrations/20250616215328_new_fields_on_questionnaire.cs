using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Tabler.Docs.Migrations
{
    /// <inheritdoc />
    public partial class new_fields_on_questionnaire : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Description",
                table: "QuestionBases",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Explanation",
                table: "QuestionBases",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Filename",
                table: "QuestionBases",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Uri",
                table: "QuestionBases",
                type: "nvarchar(max)",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Description",
                table: "QuestionBases");

            migrationBuilder.DropColumn(
                name: "Explanation",
                table: "QuestionBases");

            migrationBuilder.DropColumn(
                name: "Filename",
                table: "QuestionBases");

            migrationBuilder.DropColumn(
                name: "Uri",
                table: "QuestionBases");
        }
    }
}
