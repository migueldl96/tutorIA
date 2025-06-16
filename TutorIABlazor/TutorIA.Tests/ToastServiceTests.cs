using System.Linq;
using System.Threading;
using Tabler.Docs.Components.Modals;
using TutorIA.Services;

namespace TutorIA.Tests
{
    public class ToastServiceTests
    {
        [Fact]
        public void ToastService_is_thread_safe()
        {
            var service = new ToastService();
            const int maxWorkers = 10;
            var remainingWorkers = maxWorkers;
            var workCompletedEvent = new ManualResetEvent(false);
            for (var i = 0; i < maxWorkers; i++)
            {
                var workerNum = i;
                ThreadPool.QueueUserWorkItem(async s =>
                {
                    await service.AddToastAsync($"title-{workerNum}", "subtitle", new RenderComponent<TestModalContent>());
                    if (Interlocked.Decrement(ref remainingWorkers) == 0)
                        workCompletedEvent.Set();
                });
            }
            workCompletedEvent.WaitOne();
            workCompletedEvent.Close();
            var toastMessages = service.Toasts.ToList();
            for (var i = 0; i < maxWorkers; i++)
            {
                Assert.True(toastMessages.Any(t => t.Title == $"title-{i}"), "Element was not added to the toast list");
            }
            Assert.Equal(maxWorkers, toastMessages.Count);

        }
    }
}
