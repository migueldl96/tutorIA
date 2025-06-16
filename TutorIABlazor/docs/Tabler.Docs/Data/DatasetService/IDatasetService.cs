using System.Collections.Generic;
using System.Threading.Tasks;
using Tabler.Docs.Model.Dataset;

namespace Tabler.Docs.Data.DatasetService
{
    public interface IDatasetService
    {
        Task<ParsedUpdateDatasetResponse> UpdateDataset(UpdateDatasetRequestBody updateDatasetRequestBody);
        Task<ParsedUpdateDatasetResponse> CheckDataset();
        Task<CheckStudentDatasetResponseBody> CheckStudentDataset();
        Task<StudentStateRoasterResponseBody> GetStudentStateRoasterById(int userId);
        Task<List<StudentSkill>> GetStudentSkillsByUserIdAsync(int userId);
        Task<StudentSubject> GetStudentSubjectByUserIdAsync(int userId);
    }
}
