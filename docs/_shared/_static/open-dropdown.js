// Open the folded proof or solution that contains the target of a link.
// A link to an equation, table or figure inside a closed <details> block
// (sphinx-design dropdown) would otherwise land on a hidden element.
(function () {
  "use strict";

  function reveal() {
    var hash = window.location.hash;
    if (!hash || hash.length < 2) return;
    var target = null;
    try {
      target = document.getElementById(decodeURIComponent(hash.slice(1)));
    } catch (e) {
      return;
    }
    if (!target) return;
    var opened = false;
    for (var el = target.parentElement; el; el = el.parentElement) {
      if (el.tagName === "DETAILS" && !el.open) {
        el.open = true;
        opened = true;
      }
    }
    if (opened) target.scrollIntoView();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", reveal);
  } else {
    reveal();
  }
  window.addEventListener("hashchange", reveal);
})();
