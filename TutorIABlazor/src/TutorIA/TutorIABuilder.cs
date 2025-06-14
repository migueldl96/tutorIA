using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace TutorIA;

public class TutorIABuilder
{
    private readonly IServiceCollection services;

    public TutorIABuilder(IServiceCollection services) => this.services = services;

    public TutorIABuilder AddValidation<T>() where T : class, IFormValidator
    {
        services.Replace(ServiceDescriptor.Transient<IFormValidator, T>());
        return this;
    }
}
