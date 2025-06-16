namespace Tabler.Docs.Model.Questionnaire
{
    public abstract class QuestionBase
    {
        public int Id { get; set; }
        public string Header { get; set; } = string.Empty;
        public string? SubHeader { get; set; }
        public string Explanation { get; set; }
        public string Filename { get; set; }
        public string Description { get; set; }
        public string Uri { get; set; }
    }
}
