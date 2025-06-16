using Microsoft.Extensions.DependencyInjection;
using TutorIA.Components.Tables;
using TutorIA.Services;

namespace TutorIA
{
    public static class TablerExtensions
    {
        public static IServiceCollection AddTabler(this IServiceCollection services, Action<TablerOptions> tablerOptions = null)
        {
            if (tablerOptions is null)
            {
                tablerOptions = _ => { };
            }

            services.Configure(tablerOptions);

            return services
                .AddScoped<ToastService>()
                .AddScoped<TablerService>()
                .AddScoped<IOffcanvasService, OffcanvasService>()
                .AddScoped<IModalService, ModalService>()
                .AddScoped<TableFilterService>()
                .AddScoped<IFormValidator, TablerDataAnnotationsValidator>()
                .AddSingleton<FlagService>();
        }

        public static TutorIABuilder AddTutorIA(this IServiceCollection services, Action<TablerOptions> tablerOptions = null)
        {
            services
                .AddTabler(tablerOptions);

            return new TutorIABuilder(services);
        }
    }
}
