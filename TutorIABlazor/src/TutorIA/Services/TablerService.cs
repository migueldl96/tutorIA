using Microsoft.JSInterop;

namespace TutorIA.Services
{
    public class TablerService
    {
        private readonly IJSRuntime jsRuntime;

        public TablerService(IJSRuntime jSRuntime)
        {
            this.jsRuntime = jSRuntime;
        }

        public async Task SetTheme(bool darkTheme)
        {
            var theme = "";
            if (darkTheme)
            {
                theme = "dark";
            }

            await jsRuntime.InvokeVoidAsync("TutorIA.setTheme", theme);
        }



        public async Task<string> OpenContentWindow(string contentType, byte[] content, string urlSuffix = null, string name = null, string features = null)
        {
            return await jsRuntime.InvokeAsync<string>("TutorIA.openContentWindow", contentType, content, urlSuffix, name, features);
        }

        public async Task<string> CreateObjectURLAsync(string contentType, byte[] content)
        {
            return await jsRuntime.InvokeAsync<string>("TutorIA.createObjectURL", contentType, content);
        }

        public async Task RevokeObjectURLAsync(string objectURL)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.revokeObjectURL", objectURL);
        }

        public async Task SaveAsBinary(string fileName, string contentType, byte[] content)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.saveAsBinary", fileName, contentType, content);
        }

        public async Task SaveAsFile(string fileName, string href)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.saveAsFile", fileName, href);
        }

        public async Task PreventDefaultKey(ElementReference element, string eventName, string[] keys)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.preventDefaultKey", element, eventName, keys);
        }

        public async Task FocusFirstInTableRow(ElementReference tableRow)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.focusFirstInTableRow", tableRow, "");
        }

        public async Task NavigateTable(ElementReference tableCell, string key)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.navigateTable", tableCell, key);
        }

        public async Task ScrollToFragment(string fragmentId)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.scrollToFragment", fragmentId);
        }

        public async Task ShowAlert(string message)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.showAlert", message);
        }

        public async Task CopyToClipboard(string text)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.copyToClipboard", text);
        }

        public async Task<string> ReadFromClipboard()
        {
            return await jsRuntime.InvokeAsync<string>("TutorIA.readFromClipboard");
        }

        public async Task DisableDraggable(ElementReference container, ElementReference element)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.disableDraggable", container, element);
        }

        public async Task SetElementProperty(ElementReference element, string property, object value)
        {
            await jsRuntime.InvokeVoidAsync("TutorIA.setPropByElement", element, property, value);
        }

    }


}

