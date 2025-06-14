namespace Tabler.Docs.Model.Questionnaire
{
    public class AnswerOption
    {
        public int Id { get; set; }
        public string Text { get; set; } = string.Empty;
        public bool IsSelected { get; set; }

        public int QuestionId { get; set; }
        public UniqueChoiceQuestion Question { get; set; } = default!;
        public bool IsCorrect { get; set; }
    }
}
