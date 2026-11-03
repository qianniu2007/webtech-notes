/* =========================================================
   WebTech Notes · 共享脚本
   汉堡菜单 / 回到顶部 / 入场动画 / 代码复制 / 数字滚动
   ========================================================= */
(function () {
  "use strict";

  /* ---------- 移动端汉堡菜单 ---------- */
  const toggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");
  if (toggle && navLinks) {
    toggle.addEventListener("click", function () {
      const open = navLinks.classList.toggle("open");
      toggle.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // 点击菜单项后收起
    navLinks.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        navLinks.classList.remove("open");
        toggle.classList.remove("open");
      });
    });
  }

  /* ---------- 当前年份 ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- 回到顶部 ---------- */
  const toTop = document.querySelector(".to-top");
  if (toTop) {
    window.addEventListener("scroll", function () {
      toTop.classList.toggle("show", window.scrollY > 420);
    }, { passive: true });
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- 滚动入场动画 ---------- */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("visible"); });
  }

  /* ---------- 代码块：一键复制 ---------- */
  document.querySelectorAll(".code-block").forEach(function (block) {
    const btn = block.querySelector(".copy-btn");
    const pre = block.querySelector("pre");
    if (!btn || !pre) return;
    btn.addEventListener("click", function () {
      const text = pre.innerText;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = "已复制 ✓";
          setTimeout(function () { btn.textContent = "复制"; }, 1600);
        });
      } else {
        // 兼容回退
        const ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); btn.textContent = "已复制 ✓"; }
        catch (e) { btn.textContent = "复制失败"; }
        document.body.removeChild(ta);
        setTimeout(function () { btn.textContent = "复制"; }, 1600);
      }
    });
  });

  /* ---------- 首页数字滚动动画 ---------- */
  const counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    const animate = function (el) {
      const target = parseInt(el.getAttribute("data-count"), 10);
      const dur = 1200;
      const start = performance.now();
      function tick(now) {
        const p = Math.min((now - start) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased);
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    };
    const cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animate(entry.target);
          cio.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cio.observe(el); });
  }
})();
