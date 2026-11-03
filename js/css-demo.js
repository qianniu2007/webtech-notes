/* =========================================================
   CSS page interactions: box-model sliders + Flexbox direction/alignment
   ========================================================= */
(function () {
  "use strict";

  /* ---------- Box model: three ranges update the padding in real time ---------- */
  const marginRange = document.getElementById("marginRange");
  const borderRange = document.getElementById("borderRange");
  const paddingRange = document.getElementById("paddingRange");
  const bmMargin = document.getElementById("bmMargin");
  const bmBorder = document.getElementById("bmBorder");
  const bmPadding = document.getElementById("bmPadding");

  if (marginRange) {
    marginRange.addEventListener("input", function () {
      const v = this.value;
      bmMargin.style.padding = v + "px";
      document.getElementById("marginVal").textContent = v + "px";
    });
    borderRange.addEventListener("input", function () {
      const v = this.value;
      bmBorder.style.padding = v + "px";
      document.getElementById("borderVal").textContent = v + "px";
    });
    paddingRange.addEventListener("input", function () {
      const v = this.value;
      bmPadding.style.padding = v + "px";
      document.getElementById("paddingVal").textContent = v + "px";
    });
  }

  /* ---------- Flexbox: direction + main-axis alignment ---------- */
  const flexStage = document.getElementById("flexStage");
  const dirControl = document.getElementById("dirControl");
  const justifyControl = document.getElementById("justifyControl");

  let state = { dir: "row", jc: "flex-start" };

  function applyFlex() {
    flexStage.style.flexDirection = state.dir;
    flexStage.style.justifyContent = state.jc;
  }

  function bindGroup(group, key) {
    if (!group) return;
    group.querySelectorAll("button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        group.querySelectorAll("button").forEach(function (b) {
          b.classList.remove("on");
        });
        btn.classList.add("on");
        state[key] = btn.getAttribute("data-" + key);
        applyFlex();
      });
    });
  }

  bindGroup(dirControl, "dir");
  bindGroup(justifyControl, "jc");
})();
