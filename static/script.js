"use strict";

function _createForOfIteratorHelper(r, e) { var t = "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (!t) { if (Array.isArray(r) || (t = _unsupportedIterableToArray(r)) || e && r && "number" == typeof r.length) { t && (r = t); var _n = 0, F = function F() { }; return { s: F, n: function n() { return _n >= r.length ? { done: !0 } : { done: !1, value: r[_n++] }; }, e: function e(r) { throw r; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var o, a = !0, u = !1; return { s: function s() { t = t.call(r); }, n: function n() { var r = t.next(); return a = r.done, r; }, e: function e(r) { u = !0, o = r; }, f: function f() { try { a || null == t["return"] || t["return"](); } finally { if (u) throw o; } } }; }
function _unsupportedIterableToArray(r, a) { if (r) { if ("string" == typeof r) return _arrayLikeToArray(r, a); var t = {}.toString.call(r).slice(8, -1); return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0; } }
function _arrayLikeToArray(r, a) { (null == a || a > r.length) && (a = r.length); for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e]; return n; }
function _regenerator() { /*! regenerator-runtime -- Copyright (c) 2014-present, Facebook, Inc. -- license (MIT): https://github.com/babel/babel/blob/main/packages/babel-helpers/LICENSE */ var e, t, r = "function" == typeof Symbol ? Symbol : {}, n = r.iterator || "@@iterator", o = r.toStringTag || "@@toStringTag"; function i(r, n, o, i) { var c = n && n.prototype instanceof Generator ? n : Generator, u = Object.create(c.prototype); return _regeneratorDefine2(u, "_invoke", function (r, n, o) { var i, c, u, f = 0, p = o || [], y = !1, G = { p: 0, n: 0, v: e, a: d, f: d.bind(e, 4), d: function d(t, r) { return i = t, c = 0, u = e, G.n = r, a; } }; function d(r, n) { for (c = r, u = n, t = 0; !y && f && !o && t < p.length; t++) { var o, i = p[t], d = G.p, l = i[2]; r > 3 ? (o = l === n) && (u = i[(c = i[4]) ? 5 : (c = 3, 3)], i[4] = i[5] = e) : i[0] <= d && ((o = r < 2 && d < i[1]) ? (c = 0, G.v = n, G.n = i[1]) : d < l && (o = r < 3 || i[0] > n || n > l) && (i[4] = r, i[5] = n, G.n = l, c = 0)); } if (o || r > 1) return a; throw y = !0, n; } return function (o, p, l) { if (f > 1) throw TypeError("Generator is already running"); for (y && 1 === p && d(p, l), c = p, u = l; (t = c < 2 ? e : u) || !y;) { i || (c ? c < 3 ? (c > 1 && (G.n = -1), d(c, u)) : G.n = u : G.v = u); try { if (f = 2, i) { if (c || (o = "next"), t = i[o]) { if (!(t = t.call(i, u))) throw TypeError("iterator result is not an object"); if (!t.done) return t; u = t.value, c < 2 && (c = 0); } else 1 === c && (t = i["return"]) && t.call(i), c < 2 && (u = TypeError("The iterator does not provide a '" + o + "' method"), c = 1); i = e; } else if ((t = (y = G.n < 0) ? u : r.call(n, G)) !== a) break; } catch (t) { i = e, c = 1, u = t; } finally { f = 1; } } return { value: t, done: y }; }; }(r, o, i), !0), u; } var a = {}; function Generator() { } function GeneratorFunction() { } function GeneratorFunctionPrototype() { } t = Object.getPrototypeOf; var c = [][n] ? t(t([][n]())) : (_regeneratorDefine2(t = {}, n, function () { return this; }), t), u = GeneratorFunctionPrototype.prototype = Generator.prototype = Object.create(c); function f(e) { return Object.setPrototypeOf ? Object.setPrototypeOf(e, GeneratorFunctionPrototype) : (e.__proto__ = GeneratorFunctionPrototype, _regeneratorDefine2(e, o, "GeneratorFunction")), e.prototype = Object.create(u), e; } return GeneratorFunction.prototype = GeneratorFunctionPrototype, _regeneratorDefine2(u, "constructor", GeneratorFunctionPrototype), _regeneratorDefine2(GeneratorFunctionPrototype, "constructor", GeneratorFunction), GeneratorFunction.displayName = "GeneratorFunction", _regeneratorDefine2(GeneratorFunctionPrototype, o, "GeneratorFunction"), _regeneratorDefine2(u), _regeneratorDefine2(u, o, "Generator"), _regeneratorDefine2(u, n, function () { return this; }), _regeneratorDefine2(u, "toString", function () { return "[object Generator]"; }), (_regenerator = function _regenerator() { return { w: i, m: f }; })(); }
function _regeneratorDefine2(e, r, n, t) { var i = Object.defineProperty; try { i({}, "", {}); } catch (e) { i = 0; } _regeneratorDefine2 = function _regeneratorDefine(e, r, n, t) { function o(r, n) { _regeneratorDefine2(e, r, function (e) { return this._invoke(r, n, e); }); } r ? i ? i(e, r, { value: n, enumerable: !t, configurable: !t, writable: !t }) : e[r] = n : (o("next", 0), o("throw", 1), o("return", 2)); }, _regeneratorDefine2(e, r, n, t); }
function asyncGeneratorStep(n, t, e, r, o, a, c) { try { var i = n[a](c), u = i.value; } catch (n) { return void e(n); } i.done ? t(u) : Promise.resolve(u).then(r, o); }
function _asyncToGenerator(n) { return function () { var t = this, e = arguments; return new Promise(function (r, o) { var a = n.apply(t, e); function _next(n) { asyncGeneratorStep(a, r, o, _next, _throw, "next", n); } function _throw(n) { asyncGeneratorStep(a, r, o, _next, _throw, "throw", n); } _next(void 0); }); }; }
/* Global references */
var timelineEditor = null;
var trendingBrowser = null;
document.addEventListener('DOMContentLoaded', function () {
  var videoUrlInput = document.getElementById('videoUrl');
  var apiKeyInput = document.getElementById('apiKey');
  var generateBtn = document.getElementById('generateBtn');
  var loadBtn = document.getElementById('loadBtn');
  var editorSection = document.getElementById('editorSection');
  var editorTitle = document.getElementById('editorTitle');
  var editorCloseBtn = document.getElementById('editorCloseBtn');
  var timelineContainer = document.getElementById('timelineContainer');
  var manualGenerateBtn = document.getElementById('manualGenerateBtn');
  var previewCropBtn = document.getElementById('previewCropBtn');
  var cropSection = document.getElementById('cropSection');
  var cropContainer = document.getElementById('cropContainer');
  var cropConfirmBtn = document.getElementById('cropConfirmBtn');
  var cropCancelBtn = document.getElementById('cropCancelBtn');
  var statusSection = document.getElementById('statusSection');
  var statusTitle = document.getElementById('statusTitle');
  var jobIdDisplay = document.getElementById('jobIdDisplay');
  var progressFill = document.querySelector('.progress-fill');
  var statusDescription = document.getElementById('statusDescription');
  var resultSection = document.getElementById('resultSection');
  var shortsContainer = document.getElementById('shortsContainer');

  // Style & Overlay
  var styleSelector = document.getElementById('styleSelector');
  var overlaySelect = document.getElementById('overlaySelect');
  var overlayUpload = document.getElementById('overlayUpload');
  var currentJobId = null;
  var pollInterval = null;
  var cropSelector = null;
  var currentVideoUrl = null;
  var cropCoords = null;
  var selectedStyle = 'classico';
  var selectedOverlay = 'none';

  // ============================================
  // TABS NAVIGATION
  // ============================================
  var tabBtns = document.querySelectorAll('.tab-btn');
  var tabContents = document.querySelectorAll('.tab-content');
  tabBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = btn.dataset.tab;
      tabBtns.forEach(function (b) {
        return b.classList.remove('active');
      });
      tabContents.forEach(function (c) {
        return c.classList.remove('active');
      });
      btn.classList.add('active');
      document.getElementById("tab-".concat(target)).classList.add('active');
      if (target === 'trending' && trendingBrowser && trendingBrowser.videos.length === 0) {
        trendingBrowser.search();
      }
    });
  });

  // ============================================
  // TRENDING BROWSER
  // ============================================
  var trendingContainer = document.getElementById('trendingContainer');
  var trendingSearchInput = document.getElementById('trendingSearch');
  var trendingSearchBtn = document.getElementById('trendingSearchBtn');
  trendingBrowser = new TrendingBrowser(trendingContainer, function (url, title) {
    videoUrlInput.value = url;
    tabBtns.forEach(function (b) {
      return b.classList.remove('active');
    });
    tabContents.forEach(function (c) {
      return c.classList.remove('active');
    });
    document.querySelector('[data-tab="generator"]').classList.add('active');
    document.getElementById('tab-generator').classList.add('active');
  });
  trendingSearchBtn.addEventListener('click', function () {
    var q = trendingSearchInput.value.trim();
    if (q) trendingBrowser.search(q);
  });
  trendingSearchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      var q = trendingSearchInput.value.trim();
      if (q) trendingBrowser.search(q);
    }
  });
  document.querySelectorAll('.chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      document.querySelectorAll('.chip').forEach(function (c) {
        return c.classList.remove('active');
      });
      chip.classList.add('active');
      var q = chip.dataset.query;
      trendingSearchInput.value = q;
      trendingBrowser.search(q);
    });
  });

  // ============================================
  // SUBTITLE STYLE SELECTOR
  // ============================================
  styleSelector.querySelectorAll('.style-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      styleSelector.querySelectorAll('.style-btn').forEach(function (b) {
        return b.classList.remove('active');
      });
      btn.classList.add('active');
      selectedStyle = btn.dataset.style;
    });
  });

  // ============================================
  // OVERLAY VIDEO SELECTOR
  // ============================================
  function loadOverlayList() {
    return _loadOverlayList.apply(this, arguments);
  }
  function _loadOverlayList() {
    _loadOverlayList = _asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee5() {
      var resp, data, _iterator, _step, ov, opt, _t5;
      return _regenerator().w(function (_context5) {
        while (1) switch (_context5.p = _context5.n) {
          case 0:
            _context5.p = 0;
            _context5.n = 1;
            return fetch('/overlay-list');
          case 1:
            resp = _context5.v;
            _context5.n = 2;
            return resp.json();
          case 2:
            data = _context5.v;
            // Keep "Nenhum" option
            overlaySelect.innerHTML = '<option value="none">Nenhum overlay</option>';
            _iterator = _createForOfIteratorHelper(data.overlays || []);
            try {
              for (_iterator.s(); !(_step = _iterator.n()).done;) {
                ov = _step.value;
                opt = document.createElement('option');
                opt.value = ov.name;
                opt.textContent = "\uD83C\uDFAE ".concat(ov.label);
                overlaySelect.appendChild(opt);
              }
            } catch (err) {
              _iterator.e(err);
            } finally {
              _iterator.f();
            }
            _context5.n = 4;
            break;
          case 3:
            _context5.p = 3;
            _t5 = _context5.v;
            console.warn('Failed to load overlays', _t5);
          case 4:
            return _context5.a(2);
        }
      }, _callee5, null, [[0, 3]]);
    }));
    return _loadOverlayList.apply(this, arguments);
  }
  overlaySelect.addEventListener('change', function () {
    selectedOverlay = overlaySelect.value;
  });
  overlayUpload.addEventListener('change', /*#__PURE__*/function () {
    var _ref = _asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee(e) {
      var file, formData, resp, data, opt, _t;
      return _regenerator().w(function (_context) {
        while (1) switch (_context.p = _context.n) {
          case 0:
            file = e.target.files[0];
            if (file) {
              _context.n = 1;
              break;
            }
            return _context.a(2);
          case 1:
            formData = new FormData();
            formData.append('file', file);
            _context.p = 2;
            _context.n = 3;
            return fetch('/upload-overlay-file', {
              method: 'POST',
              body: formData
            });
          case 3:
            resp = _context.v;
            if (resp.ok) {
              _context.n = 4;
              break;
            }
            throw new Error('Upload falhou');
          case 4:
            _context.n = 5;
            return resp.json();
          case 5:
            data = _context.v;
            // Add to dropdown and select
            opt = document.createElement('option');
            opt.value = data.name;
            opt.textContent = "\uD83D\uDCE4 ".concat(data.label);
            overlaySelect.appendChild(opt);
            overlaySelect.value = data.name;
            selectedOverlay = data.name;
            _context.n = 7;
            break;
          case 6:
            _context.p = 6;
            _t = _context.v;
            alert('Erro no upload: ' + _t.message);
          case 7:
            return _context.a(2);
        }
      }, _callee, null, [[2, 6]]);
    }));
    return function (_x) {
      return _ref.apply(this, arguments);
    };
  }());

  // Load overlays on startup
  loadOverlayList();

  // ============================================
  // LOAD VIDEO (MANUAL MODE)
  // ============================================
  loadBtn.addEventListener('click', /*#__PURE__*/_asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee2() {
    var url, response, err, data, _t2;
    return _regenerator().w(function (_context2) {
      while (1) switch (_context2.p = _context2.n) {
        case 0:
          url = videoUrlInput.value.trim();
          if (url) {
            _context2.n = 1;
            break;
          }
          alert('Insira um link de vídeo.');
          return _context2.a(2);
        case 1:
          currentVideoUrl = url;
          setBtnLoading(loadBtn, true);
          _context2.p = 2;
          _context2.n = 3;
          return fetch('/load', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              url: url
            })
          });
        case 3:
          response = _context2.v;
          if (response.ok) {
            _context2.n = 5;
            break;
          }
          _context2.n = 4;
          return response.json()["catch"](function () {
            return {};
          });
        case 4:
          err = _context2.v;
          throw new Error(err.detail || 'Falha ao carregar vídeo');
        case 5:
          _context2.n = 6;
          return response.json();
        case 6:
          data = _context2.v;
          editorSection.classList.remove('hidden');
          resultSection.classList.add('hidden');
          statusSection.classList.add('hidden');
          cropSection.classList.add('hidden');
          editorTitle.textContent = "\uD83D\uDCF9 ".concat(data.title);
          timelineEditor = new TimelineEditor(timelineContainer, data.video_url, data.duration, data.captions);
          cropCoords = null;
          previewCropBtn.textContent = '✂️ Selecionar Área de Crop';
          editorSection.scrollIntoView({
            behavior: 'smooth'
          });
          _context2.n = 8;
          break;
        case 7:
          _context2.p = 7;
          _t2 = _context2.v;
          alert('Erro: ' + _t2.message);
        case 8:
          _context2.p = 8;
          setBtnLoading(loadBtn, false);
          return _context2.f(8);
        case 9:
          return _context2.a(2);
      }
    }, _callee2, null, [[2, 7, 8, 9]]);
  })));

  // ============================================
  // CLOSE EDITOR
  // ============================================
  editorCloseBtn.addEventListener('click', function () {
    editorSection.classList.add('hidden');
    cropSection.classList.add('hidden');
    timelineEditor = null;
  });

  // ============================================
  // CROP SELECTION
  // ============================================
  previewCropBtn.addEventListener('click', /*#__PURE__*/_asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee3() {
    var resp, data, _t3;
    return _regenerator().w(function (_context3) {
      while (1) switch (_context3.p = _context3.n) {
        case 0:
          if (currentVideoUrl) {
            _context3.n = 1;
            break;
          }
          return _context3.a(2);
        case 1:
          setBtnLoading(previewCropBtn, true);
          _context3.p = 2;
          _context3.n = 3;
          return fetch('/preview', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              url: currentVideoUrl
            })
          });
        case 3:
          resp = _context3.v;
          if (resp.ok) {
            _context3.n = 4;
            break;
          }
          throw new Error('Falha ao carregar preview');
        case 4:
          _context3.n = 5;
          return resp.json();
        case 5:
          data = _context3.v;
          cropSection.classList.remove('hidden');
          cropSelector = new CropSelector(cropContainer, data.preview_url, data.video_width, data.video_height);
          cropSection.scrollIntoView({
            behavior: 'smooth'
          });
          _context3.n = 7;
          break;
        case 6:
          _context3.p = 6;
          _t3 = _context3.v;
          alert('Erro: ' + _t3.message);
        case 7:
          _context3.p = 7;
          setBtnLoading(previewCropBtn, false);
          return _context3.f(7);
        case 8:
          return _context3.a(2);
      }
    }, _callee3, null, [[2, 6, 7, 8]]);
  })));
  cropConfirmBtn.addEventListener('click', function () {
    if (cropSelector) {
      cropCoords = cropSelector.getNormalizedCenter();
      previewCropBtn.textContent = "\u2702\uFE0F Crop: ".concat((cropCoords.x * 100).toFixed(0), "%, ").concat((cropCoords.y * 100).toFixed(0), "%");
    }
    cropSection.classList.add('hidden');
  });
  cropCancelBtn.addEventListener('click', function () {
    return cropSection.classList.add('hidden');
  });

  // ============================================
  // GENERATE: MANUAL SEGMENTS
  // ============================================
  manualGenerateBtn.addEventListener('click', function () {
    if (!timelineEditor || !currentVideoUrl) return;
    var segments = timelineEditor.getSegments();
    if (segments.length === 0) {
      alert('Selecione segmentos antes de gerar!');
      return;
    }
    var body = {
      url: currentVideoUrl,
      segments: segments,
      sub_style: selectedStyle,
      overlay_video: selectedOverlay !== 'none' ? selectedOverlay : null
    };
    if (cropCoords) {
      body.crop_x = cropCoords.x;
      body.crop_y = cropCoords.y;
    }
    startProcessing('/process-manual', body);
  });

  // ============================================
  // GENERATE: AI AUTO
  // ============================================
  generateBtn.addEventListener('click', function () {
    var url = videoUrlInput.value.trim();
    if (!url) {
      alert('Insira um link de vídeo.');
      return;
    }
    var body = {
      url: url,
      api_key: apiKeyInput.value.trim() || null,
      sub_style: selectedStyle,
      overlay_video: selectedOverlay !== 'none' ? selectedOverlay : null
    };
    if (cropCoords) {
      body.crop_x = cropCoords.x;
      body.crop_y = cropCoords.y;
    }
    startProcessing('/process', body);
  });

  // ============================================
  // PROCESSING CORE
  // ============================================
  function startProcessing(_x2, _x3) {
    return _startProcessing.apply(this, arguments);
  }
  function _startProcessing() {
    _startProcessing = _asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee6(endpoint, body) {
      var resp, err, data, _t6;
      return _regenerator().w(function (_context6) {
        while (1) switch (_context6.p = _context6.n) {
          case 0:
            setLoading(true);
            resultSection.classList.add('hidden');
            shortsContainer.innerHTML = '';
            _context6.p = 1;
            _context6.n = 2;
            return fetch(endpoint, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(body)
            });
          case 2:
            resp = _context6.v;
            if (resp.ok) {
              _context6.n = 4;
              break;
            }
            _context6.n = 3;
            return resp.json()["catch"](function () {
              return {};
            });
          case 3:
            err = _context6.v;
            throw new Error(err.detail || 'Falha ao iniciar');
          case 4:
            _context6.n = 5;
            return resp.json();
          case 5:
            data = _context6.v;
            currentJobId = data.job_id;
            statusSection.classList.remove('hidden');
            jobIdDisplay.textContent = "JobID: #".concat(currentJobId.substring(0, 8));
            updateProgress(10, 'Iniciando processamento...');
            startPolling();
            _context6.n = 7;
            break;
          case 6:
            _context6.p = 6;
            _t6 = _context6.v;
            alert('Erro: ' + _t6.message);
            setLoading(false);
          case 7:
            return _context6.a(2);
        }
      }, _callee6, null, [[1, 6]]);
    }));
    return _startProcessing.apply(this, arguments);
  }
  function startPolling() {
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(/*#__PURE__*/_asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee4() {
      var resp, data, _t4;
      return _regenerator().w(function (_context4) {
        while (1) switch (_context4.p = _context4.n) {
          case 0:
            if (currentJobId) {
              _context4.n = 1;
              break;
            }
            return _context4.a(2);
          case 1:
            _context4.p = 1;
            _context4.n = 2;
            return fetch("/status/".concat(currentJobId));
          case 2:
            resp = _context4.v;
            if (resp.ok) {
              _context4.n = 3;
              break;
            }
            throw new Error();
          case 3:
            _context4.n = 4;
            return resp.json();
          case 4:
            data = _context4.v;
            if (data.status === 'processing') {
              updateProgress(40, 'Processando segmentos...');
            } else if (data.status === 'completed') {
              stopPolling();
              updateProgress(100, 'Concluído!');
              showResults(data.shorts);
              setLoading(false);
            } else if (data.status === 'failed') {
              stopPolling();
              updateProgress(0, 'Erro');
              statusTitle.textContent = 'Falha';
              statusDescription.textContent = data.error || 'Erro desconhecido.';
              setLoading(false);
            }
            _context4.n = 6;
            break;
          case 5:
            _context4.p = 5;
            _t4 = _context4.v;
            stopPolling();
            setLoading(false);
          case 6:
            return _context4.a(2);
        }
      }, _callee4, null, [[1, 5]]);
    })), 3000);
  }
  function stopPolling() {
    if (pollInterval) {
      clearInterval(pollInterval);
      pollInterval = null;
    }
  }
  function updateProgress(pct, text) {
    progressFill.style.width = "".concat(pct, "%");
    statusDescription.textContent = text;
  }
  function setLoading(on) {
    generateBtn.disabled = on;
    generateBtn.querySelector('.btn-text').classList.toggle('hidden', on);
    generateBtn.querySelector('.loader-ring').classList.toggle('hidden', !on);
  }
  function setBtnLoading(btn, on) {
    var text = btn.querySelector('.btn-text') || btn;
    var loader = btn.querySelector('.loader-ring');
    if (loader) {
      btn.disabled = on;
      text.classList.toggle('hidden', on);
      loader.classList.toggle('hidden', !on);
    } else {
      btn.disabled = on;
    }
  }
  function showResults(shorts) {
    resultSection.classList.remove('hidden');
    shortsContainer.innerHTML = '';
    if (!shorts || shorts.length === 0) {
      shortsContainer.innerHTML = '<p>Nenhum short gerado.</p>';
      return;
    }
    shorts.forEach(function (_short, i) {
      var path = _short.path.replace(/\\/g, '/');
      var videoUrl = "/".concat(path.split('/').slice(-2).join('/'));
      var card = document.createElement('div');
      card.className = 'short-card';
      card.innerHTML = "\n                <div class=\"video-preview\"><video src=\"".concat(videoUrl, "\" controls></video></div>\n                <div class=\"short-info\">\n                    <p>").concat(_short.reason || 'Segmento selecionado.', "</p>\n                    <div class=\"short-actions\">\n                        <a href=\"").concat(videoUrl, "\" download class=\"btn-download\">Baixar Short</a>\n                        <a href=\"/export-package/").concat(currentJobId, "/").concat(i, "\" download class=\"btn-export\" title=\"Baixar pacote com elementos separados para edi\u00e7\u00e3o\">📦 Pacote de Edi\u00e7\u00e3o</a>\n                    </div>\n                </div>\n            ");
      shortsContainer.appendChild(card);
    });
    resultSection.scrollIntoView({
      behavior: 'smooth'
    });
  }
});
