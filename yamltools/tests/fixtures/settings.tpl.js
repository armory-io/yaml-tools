var gateUrl = '${services.deck.gateUrl}';
var authEnabled = '${services.deck.auth.enabled}';
window.spinnakerSettings = {
  gateUrl: gateUrl,
  bakeryDetailUrl: gateUrl + '/bakery/logs/global/{{context.status.id}}',
};
