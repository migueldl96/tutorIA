using System.Collections.Generic;
using Tabler.Docs.Model.Auth;

namespace Tabler.Docs.Data.AuthService
{
    public interface IAuthService
    {
        IEnumerable<User> GetUsers();
        User GetUserById(int id);
    }
}
