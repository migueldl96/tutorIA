using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Tabler.Docs.Model.Dataset;

namespace Tabler.Docs.Data.DatasetService
{
    public class DatasetService : IDatasetService
    {
        private readonly ApplicationDbContext _dbContext;
        private readonly HttpClient _http;
        public DatasetService(ApplicationDbContext dbContext, IHttpClientFactory httpClientFactory)
        {
            _dbContext = dbContext;
            _http = httpClientFactory.CreateClient("StudentEvalApiClient");
        }

        public async Task<ParsedUpdateDatasetResponse> CheckDataset()
        {
            var response = await _http.PostAsync("/evaluation/get_model_status", null);
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            var items = JsonSerializer.Deserialize<List<Class1>>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (items == null)
            {
                throw new Exception("Failed to deserialize response from UpdateDataset");
            }

            var wrapped = new UpdateDatasetResponseBody { Items = items };
            var parsed = ParseUpdateDatasetResponseToEntities(wrapped);

            _dbContext.StudentSubjects.RemoveRange(_dbContext.StudentSubjects);
            _dbContext.SubjectSkills.RemoveRange(_dbContext.SubjectSkills);
            _dbContext.SaveChanges();

            _dbContext.StudentSubjects.AddRange(parsed.StudentSubjects);
            _dbContext.SubjectSkills.AddRange(parsed.SubjectSkills);
            _dbContext.SaveChanges();

            return parsed!;
        }

        public async Task<CheckStudentDatasetResponseBody> CheckStudentDataset()
        {
            var response = await _http.PostAsync("/evaluation/check_students_dataset", null);
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<CheckStudentDatasetResponseBody>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (result == null)
            {
                throw new Exception("Failed to deserialize response from CheckDataset");
            }

            // Procesar manualmente el campo `data`
            if (result.data.ValueKind == JsonValueKind.Array)
            {
                result.ParsedData = result.data
                    .EnumerateArray()
                    .Select(element => JsonSerializer.Deserialize<Datum>(element.GetRawText()))
                    .Where(x => x != null)
                    .ToList()!;
            }
            else
            {
                result.ParsedData = new List<Datum>();
            }

            return result;
        }


        public async Task<ParsedUpdateDatasetResponse> UpdateDataset(UpdateDatasetRequestBody updateDatasetRequestBody)
        {
            var content = new StringContent(
                JsonSerializer.Serialize(updateDatasetRequestBody),
                Encoding.UTF8,
                "application/json"
            );

            var response = await _http.PostAsync("/evaluation/update_dataset", content);
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            var items = JsonSerializer.Deserialize<List<Class1>>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (items == null)
            {
                throw new Exception("Failed to deserialize response from UpdateDataset");
            }

            var wrapped = new UpdateDatasetResponseBody { Items = items };
            var parsed = ParseUpdateDatasetResponseToEntities(wrapped);

            return parsed!;
        }


        private static ParsedUpdateDatasetResponse ParseUpdateDatasetResponseToEntities(UpdateDatasetResponseBody response)
        {
            var studentSubjects = new List<StudentSubject>();
            var subjectSkills = new List<SubjectSkill>();

            foreach (var item in response.Items)
            {
                // Parse students_states
                foreach (var studentState in item.students_states)
                {

                    foreach (var subject in studentState.student_subject_list)
                    {
                        var studentSubject = new StudentSubject
                        {
                            Name = subject.subject_name,
                            UserId = int.Parse(studentState.id),
                            Skills = subject.student_skill_list.Select(skill => new StudentSkill
                            {
                                Name = skill.name,
                                Learn = skill.learn
                            }).ToList()
                        };

                        studentSubjects.Add(studentSubject);
                    }
                }

                // Parse skills_states
                foreach (var skillState in item.skills_states)
                {
                    var subjectSkill = new SubjectSkill
                    {
                        Name = skillState.skill_name,
                        SubjectDetails = skillState.subject_skill_list.Select(detail => new SubjectSkillDetail
                        {
                            Name = detail.subject_skill_name,
                            States = detail.states.Select(s => new SkillState
                            {
                                Name = s.name,
                                Value = s.value
                            }).ToList()
                        }).ToList()
                    };

                    subjectSkills.Add(subjectSkill);
                }
            }

            return new() { StudentSubjects = studentSubjects, SubjectSkills = subjectSkills };
        }

        public Task<List<StudentSkill>> GetStudentSkillsByUserIdAsync(int userId)
        {
            return _dbContext.StudentSkills
                .Include(ss => ss.StudentSubject)
                .Include(ss => ss.StudentSubject.Skills)
                .Where(ss => ss.StudentSubject.UserId == userId)
                .ToListAsync();
        }

        public async Task<StudentSubject> GetStudentSubjectByUserIdAsync(int userId)
        {
            return _dbContext.StudentSubjects
                .Include(ss => ss.Skills)
                .Where(ss => ss.UserId == userId).FirstOrDefault();
        }

        public async Task<StudentStateRoasterResponseBody> GetStudentStateRoasterById(int userId)
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

            var response = await _http.PostAsync("/evaluation/get_student_state_roaster", content);
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<List<StudentStateRoasterResponseBody>>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (result == null)
            {
                throw new Exception("Failed to deserialize response from StudentStateRoaster");
            }


            return result.FirstOrDefault()!;
        }
    }
}
