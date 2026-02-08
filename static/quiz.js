(function () {
  function qs(id){ return document.getElementById(id); }

  // Timer apenas no modo prova
  var limit = window.LEXQUIZ_TIME_LIMIT;
  if (!limit) return;

  var bar = qs("timerBar");
  var text = qs("timerText");
  var start = Date.now();
  var total = limit * 1000;

  var tick = setInterval(function () {
    var elapsed = Date.now() - start;
    var left = Math.max(0, total - elapsed);
    var pct = left / total;

    if (bar) bar.style.transform = "scaleX(" + pct + ")";
    if (text) text.textContent = Math.ceil(left / 1000) + "s";

    if (left <= 0) {
      clearInterval(tick);
      // Se estourou o tempo, envia sem escolha (vai como -1 no backend)
      var form = document.querySelector("form.choices");
      if (form) {
        var hidden = document.createElement("input");
        hidden.type = "hidden";
        hidden.name = "choice";
        hidden.value = "-1";
        form.appendChild(hidden);
        form.submit();
      }
    }
  }, 120);
})();
