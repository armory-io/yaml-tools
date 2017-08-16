var gateUrl = ${services.deck.gateUrl};
var authEnabled = ${services.deck.auth.enabled};
var canaryEnabled = ${services.deck.canary.enabled};
window.spinnakerSettings = {
  gateUrl: gateUrl,
  bakeryDetailUrl: gateUrl + '/bakery/logs/global/{{context.status.id}}',
  canaryEnabled: canaryEnabled
};
