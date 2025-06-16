using System.Collections.Generic;
using System.Threading.Tasks;
using Tabler.Docs.Model.Evaluation;
using Tabler.Docs.Model.Questionnaire;

namespace Tabler.Docs.Data.QuestionnaireService
{
    public interface IQuestionnaireService
    {
        Task<List<QuestionBase>> RequestQuestionsToAi(string topic, string difficulty, int numQuestions);
        Task<List<QuestionBase>> GetQuestionByIdsAsync(int[] id);
        Task<StartRealTimeEvaluationResponse> StartRealTimeEvaluation(int userId, string[] skillNames);
        Task<RealTimeEvaluationIterationResponse> IterateRealTimeEvaluationAsync(
    int userId,
    string skillName,
    int correct,
    string itemId,
    string subjectId,
    string roasterPath);
        Task<List<GetStudentStateRoasterResponse>> GetStudentStateRoaster(int userId);
    }
}
