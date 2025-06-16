using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Tabler.Docs.Model.Evaluation;
using Tabler.Docs.Model.Questionnaire;

namespace Tabler.Docs.Data.QuestionnaireService
{
    public class QuestionnaireService : IQuestionnaireService
    {
        private readonly ApplicationDbContext _dbContext;
        private readonly HttpClient _contentGeneratorHttpClient;
        private readonly HttpClient _studentEvalHttpClient;
        public QuestionnaireService(ApplicationDbContext dbContext, IHttpClientFactory httpClientFactory)
        {
            _dbContext = dbContext;
            _contentGeneratorHttpClient = httpClientFactory.CreateClient("ContentGeneratorApiClient");
            _studentEvalHttpClient = httpClientFactory.CreateClient("StudentEvalApiClient");
        }

        public async Task<List<QuestionBase>> RequestQuestionsToAi(string topic, string difficulty, int numQuestions)
        {
            var payload = new
            {
                topic,
                difficulty,
                num_questions = numQuestions
            };

            var content = new StringContent(
                JsonSerializer.Serialize(payload),
                Encoding.UTF8,
                "application/json"
            );

            var response = await _contentGeneratorHttpClient.PostAsync("/api/v1/quiz/generate", content);
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            var rawQuestions = JsonSerializer.Deserialize<List<Class1>>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (rawQuestions == null)
                return new();

            var result = rawQuestions.Select(q => new UniqueChoiceQuestion
            {
                Header = q.question,
                SubHeader = q.description,
                Options = new List<AnswerOption>
        {
            new() { Text = q.optionA, IsCorrect = q.correct_answer.Equals("A", StringComparison.OrdinalIgnoreCase) },
            new() { Text = q.optionB, IsCorrect = q.correct_answer.Equals("B", StringComparison.OrdinalIgnoreCase) },
            new() { Text = q.optionC, IsCorrect = q.correct_answer.Equals("C", StringComparison.OrdinalIgnoreCase) },
            new() { Text = q.optionD, IsCorrect = q.correct_answer.Equals("D", StringComparison.OrdinalIgnoreCase) }
        }
            }).Cast<QuestionBase>().ToList();

            _dbContext.QuestionBases.AddRange(result);
            _dbContext.SaveChanges();

            return result;
        }

        public async Task<List<QuestionBase>> GetQuestionByIdsAsync(int[] ids)
        {
            var questions = await _dbContext.QuestionBases
        .Where(q => ids.Contains(q.Id))
        .ToListAsync();

            // Cargar manualmente las opciones solo para las preguntas UniqueChoice
            var UniqueChoiceQuestions = questions
                .OfType<UniqueChoiceQuestion>()
                .ToList();

            await _dbContext.Entry(UniqueChoiceQuestions[0])
                .Collection(q => q.Options)
                .LoadAsync();

            foreach (var mcq in UniqueChoiceQuestions)
            {
                await _dbContext.Entry(mcq)
                    .Collection(q => q.Options)
                    .LoadAsync();
            }

            return questions;
        }

        public async Task<StartRealTimeEvaluationResponse> StartRealTimeEvaluation(int userId, string[] skillNames)
        {
            var payload = new
            {
                user_id = userId.ToString(),
                skill_names = skillNames
            };

            var content = new StringContent(
                JsonSerializer.Serialize(payload),
                Encoding.UTF8,
                "application/json"
            );

            var response = await _studentEvalHttpClient.PostAsync("/evaluation/start_real_time_evaluation", content);
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<StartRealTimeEvaluationResponse>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            return result!;
        }

        public async Task<RealTimeEvaluationIterationResponse> IterateRealTimeEvaluationAsync(
    int userId,
    string skillName,
    int correct,
    string itemId,
    string subjectId,
    string roasterPath)
        {
            var payload = new
            {
                order_id = _dbContext.Users.Where(u => u.Id == userId).FirstOrDefault().LastQuestionOrderId,
                user_id = userId.ToString(),
                skill_name = skillName,
                correct = correct,
                item_id = itemId,
                subject_id = subjectId,
                roaster_path = roasterPath
            };

            var content = new StringContent(
                JsonSerializer.Serialize(payload),
                Encoding.UTF8,
                "application/json"
            );

            var response = await _studentEvalHttpClient.PostAsync("/evaluation/real_time_evaluation", content);
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<RealTimeEvaluationIterationResponse>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            _dbContext.Users.Where(u => u.Id == userId).FirstOrDefault().LastQuestionOrderId++;
            _dbContext.SaveChanges();

            return result!;
        }

        public async Task<List<GetStudentStateRoasterResponse>> GetStudentStateRoaster(int userId)
        {
            var payload = new
            {
                user_id = userId.ToString()
            };

            var content = new StringContent(
                JsonSerializer.Serialize(payload),
                Encoding.UTF8,
                "application/json"
            );

            var response = await _studentEvalHttpClient.PostAsync("/evaluation/get_student_state_roaster", content);
            if (!response.IsSuccessStatusCode)
            {
                return null;
            }

            var json = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<List<GetStudentStateRoasterResponse>>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });


            return result!;
        }
    }
}
