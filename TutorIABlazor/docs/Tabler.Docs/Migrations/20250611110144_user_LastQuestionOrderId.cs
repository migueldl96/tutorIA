using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Tabler.Docs.Migrations
{
    /// <inheritdoc />
    public partial class user_LastQuestionOrderId : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "LastQuestionOrderId",
                table: "Users",
                type: "int",
                nullable: false,
                defaultValue: 0);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "LastQuestionOrderId",
                table: "Users");
        }
    }
}
