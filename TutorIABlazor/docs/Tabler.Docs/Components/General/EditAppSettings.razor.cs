using Microsoft.AspNetCore.Components;
using Tabler.Docs.Services;
using TutorIA;
using TutorIA.Services;

namespace Tabler.Docs.Components.General
{
    public partial class EditAppSettings : ComponentBase
    {
        [Inject] private AppService appService { get; set; }
        [Inject] private TablerService tablerService { get; set; }


        private AppSettings settings => appService.Settings;

        private void SetNavBackground(NavbarBackground navBackground)
        {
            settings.NavbarBackground = navBackground;
            appService.SettingsUpdated();
        }

        private void SetNavDirection(NavbarDirection navbarDirection)
        {
            settings.NavbarDirection = navbarDirection;
            appService.SettingsUpdated();
        }


        private async void SetDarkMode(bool value)
        {
            settings.DarkMode = value;
            appService.SettingsUpdated();
            await tablerService.SetTheme(value);

        }


    }
}

