// Assembles the email address and the phone number in the browser, so that
// the page source never contains them in a form that scrapers recognise.
// Without JavaScript the <noscript> text next to each link is shown instead.
(function () {
  "use strict";
  var emails = document.querySelectorAll("a.contact-email");
  for (var i = 0; i < emails.length; i++) {
    var a = emails[i];
    var u = a.getAttribute("data-u");
    var d = a.getAttribute("data-d");
    if (!u || !d) { continue; }
    var address = u + "@" + d;
    a.setAttribute("href", "mailto:" + address);
    a.textContent = address;
  }
  var phones = document.querySelectorAll("a.contact-phone");
  for (var j = 0; j < phones.length; j++) {
    var p = phones[j];
    var parts = (p.getAttribute("data-p") || "").split("-");
    if (parts.length < 2) { continue; }
    p.setAttribute("href", "tel:+" + parts.join(""));
    p.textContent = "+" + parts.join(" ");
  }
})();
