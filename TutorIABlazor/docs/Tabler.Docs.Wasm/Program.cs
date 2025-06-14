using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Tabler.Docs.Data.AuthService;
using Tabler.Docs.Services;
using TutorIA.QuickTable.EntityFramework;

namespace Tabler.Docs.Wasm
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebAssemblyHostBuilder.CreateDefault(args);
            builder.RootComponents.Add<App>("#app");
            builder.Services.AddHttpClient("Local", client => client.BaseAddress = new Uri(builder.HostEnvironment.BaseAddress));
            builder.Services.AddHttpClient("GitHub", client => client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("TutorIA", "1")));
            builder.Services.AddDocs();
            builder.Services.AddScoped<ICodeSnippetService, GitHubSnippetService>();
            builder.Services.AddScoped<IDataService, LocalDataService>();
            builder.Services.AddScoped<IAuthService, AuthService>();
            builder.Services.AddDbContextFactory<ApplicationDbContext>(options => options.UseSqlite("Data Source=app.db"));
            builder.Services.AddQuickTableEntityFrameworkAdapter();


            await builder.Build().RunAsync();
        }
    }
}

