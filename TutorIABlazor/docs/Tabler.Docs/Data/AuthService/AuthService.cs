using System.Collections.Generic;
using System.Linq;
using Tabler.Docs.Model.Auth;

namespace Tabler.Docs.Data.AuthService
{
    public class AuthService : IAuthService
    {
        private readonly ApplicationDbContext _dbContext;
        public AuthService(ApplicationDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public User GetUserById(int id)
        {
            return _dbContext.Users.Where(x => x.Id == id).FirstOrDefault();
        }

        public IEnumerable<User> GetUsers()
        {
            return _dbContext.Users.ToList();
        }
    }
}
