using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;

namespace Tabler.Docs.Model.Questionnaire
{
    public class UniqueChoiceQuestion : QuestionBase
    {
        public List<AnswerOption> Options { get; set; } = new();
        [NotMapped]
        public bool IsCorrect { get; set; }
    }
}
