// TEST_ONLY. Only the fixed probe may hide a tab from its localhost fixture.
browser.runtime.onMessageExternal.addListener(async (message, sender) => {
  if (sender.id !== "f01-probe@windowsafe.invalid" || message.operation !== "hide") {
    throw new Error("Unauthorized synthetic helper request");
  }
  const tab = await browser.tabs.get(message.tabId);
  if (!tab.url || !/^http:\/\/127\.0\.0\.1:\d+\/article\.html/.test(tab.url) || tab.incognito) {
    throw new Error("Synthetic tab required");
  }
  return browser.tabs.hide(message.tabId);
});
