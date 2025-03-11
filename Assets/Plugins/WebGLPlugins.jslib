mergeInto(LibraryManager.library, {
  OnBalanceUpdated: function (balanceStr) {
    console.log("Unity OnBalanceUpdated called with:", balanceStr);
    var balance = UTF8ToString(balanceStr);
    console.log("Converted balance:", balance);
    if (window.onBalanceUpdated) {
      console.log("window.onBalanceUpdated exists, calling it");
      window.onBalanceUpdated(balance);
      console.log("window.onBalanceUpdated called");
    } else {
      console.error("onBalanceUpdated function not found in browser context");
    }
  },
});
