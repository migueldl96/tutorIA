namespace Tabler.Docs.Model.Questionnaire
{
    public abstract class QuestionBase
    {
        public int Id { get; set; }
        public string Header { get; set; } = string.Empty;
        public string? SubHeader { get; set; }
    }
}
