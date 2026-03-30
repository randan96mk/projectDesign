/**
 * ============================================================
 *  Campaign Orchestration Platform — Data Flow Diagram (DFD)
 *  Miro Board Script  ·  Paste into Chrome DevTools Console
 *  while on your Miro board tab  (app.miro.com)
 * ============================================================
 *
 *  USAGE:
 *    1. Open your Miro board in Chrome
 *    2. Press F12 → Console tab
 *    3. Paste this entire script and press Enter
 *    4. Watch progress logs (~25 s to complete)
 *    5. Press Ctrl+Shift+H to fit the full diagram on screen
 *
 *  LAYOUT (left → right):
 *    External Entities  |  Fusion Processes (P1-P7)
 *    |  Adobe I/O Runtime (5 actions)  |  Data Stores (D1-D5)
 *    |  Integration + Target (P6, Marketo)
 * ============================================================
 */

(async () => {

  if (typeof miro === 'undefined' || !miro.board) {
    console.error('❌ Not on a Miro board. Open app.miro.com first.');
    return;
  }

  console.log('🚀 Building DFD — please wait...');
  const b = miro.board;
  const n = {}; // id registry  key → miro item id

  // ── STYLE HELPERS ─────────────────────────────────────────
  // Only properties accepted by Miro SDK v2:
  //   Shape:     fillColor, borderColor, borderWidth (int), borderStyle,
  //              textAlign, textAlignVertical, fontSize (int), color
  //   Connector: startStrokeCap, endStrokeCap, strokeColor,
  //              strokeWidth (int), strokeStyle
  //   Text:      textAlign, fontSize (int), color

  const ss = (fill, border, bw, textColor, fs, align) => ({
    fillColor         : fill,
    borderColor       : border,
    borderWidth       : Math.round(bw),
    borderStyle       : 'normal',
    textAlign         : align || 'center',
    textAlignVertical : 'middle',
    fontSize          : Math.round(fs),
    color             : textColor,
  });

  const sd = (fill, border, textColor, fs) => ({   // dashed border variant
    fillColor         : fill,
    borderColor       : border,
    borderWidth       : 1,
    borderStyle       : 'dashed',
    textAlign         : 'center',
    textAlignVertical : 'middle',
    fontSize          : Math.round(fs),
    color             : textColor,
  });

  // ── HELPERS ────────────────────────────────────────────────
  const S = async (key, opts) => {
    console.log(`  shape: ${key}`);
    const s = await b.createShape(opts);
    n[key] = s.id;
    return s;
  };

  const C = async (from, to, label, opts = {}) => {
    console.log(`  conn: ${from} → ${to}`);
    await b.createConnector({
      shape : 'elbowed',
      style : {
        startStrokeCap : 'none',
        endStrokeCap   : 'arrow',
        strokeColor    : opts.color  || '#888888',
        strokeWidth    : opts.thick  ? 3 : 2,
        strokeStyle    : opts.dashed ? 'dashed' : 'normal',
      },
      start    : { item: n[from], position: opts.sp || { x: 0.5, y: 1   } },
      end      : { item: n[to],   position: opts.ep || { x: 0.5, y: 0   } },
      captions : label ? [{ content: label, position: 0.5 }] : [],
    });
  };

  // ── COLOURS ───────────────────────────────────────────────
  const RED    = '#FA0F00';
  const BLUE   = '#1473E6';
  const GREEN  = '#12805C';
  const PURPLE = '#7C3AED';
  const ORANGE = '#E68619';
  const DARK   = '#2C2C2C';

  // ── LAYOUT ────────────────────────────────────────────────
  //  x=-650  External entities (left)
  //  x=0     Fusion processes  P1-P7
  //  x=420   Adobe I/O Runtime actions  (NEW)
  //  x=820   Data stores  D1-D5
  //  x=820   Integration  P6 / Marketo (shifted right)

  const L = {
    // External entities
    marketer : { x: -650, y: -380 },
    opsTeam  : { x: -650, y:  380 },
    marketo  : { x: 1100, y:  380 },
    // SFDC note
    sfdc     : { x: -650, y: -560 },
    // Fusion processes
    p1: { x:   0, y: -380 },
    p2: { x:   0, y: -200 },
    p3: { x:   0, y:  -20 },
    p4: { x:   0, y:  160 },
    p5: { x:   0, y:  380 },
    p6: { x:   0, y:  560 },
    p7: { x:   0, y:  740 },
    // Adobe I/O Runtime actions (new column)
    io_validation   : { x: 420, y: -380 },
    io_overview     : { x: 420, y: -200 },
    io_ops_overview : { x: 420, y:  160 },
    io_sync_build   : { x: 420, y:  380 },
    io_response_proc: { x: 420, y:  740 },
    // Data stores
    d1: { x: 820, y: -380 },
    d2: { x: 820, y: -280 },
    d3: { x: 820, y: -180 },
    d4: { x: 820, y:  -80 },
    d5: { x: 820, y:   20 },
  };

  try {

    // ── TITLE ───────────────────────────────────────────────
    console.log('  text: title');
    await b.createText({
      content : 'Campaign Orchestration Platform — Data Flow Diagram (DFD)',
      x: 150, y: -780, width: 1100,
      style: { textAlign: 'center', fontSize: 22, color: DARK },
    });
    await b.createText({
      content : 'Level-1 DFD  ·  APAC / AMER scope  ·  Adobe Campaign Orchestration',
      x: 150, y: -740, width: 1100,
      style: { textAlign: 'center', fontSize: 13, color: '#888888' },
    });

    // ── LEGEND ──────────────────────────────────────────────
    const legs = [
      { lbl: 'External Entity',       fill: '#FFF0EF', border: RED    },
      { lbl: 'Fusion Process (Pn)',   fill: '#EAF2FF', border: BLUE   },
      { lbl: 'Adobe I/O Action',      fill: '#F1ECFE', border: PURPLE },
      { lbl: 'Data Store (Dn)',       fill: '#E6F5F0', border: GREEN  },
      { lbl: 'SFDC Note',             fill: '#FFFDE7', border: ORANGE },
    ];
    let lx = -700;
    for (const leg of legs) {
      console.log(`  legend: ${leg.lbl}`);
      await b.createShape({
        type: 'shape', shape: 'rectangle',
        content: leg.lbl,
        x: lx, y: -680, width: 168, height: 38,
        style: ss(leg.fill, leg.border, 2, DARK, 11),
      });
      lx += 182;
    }

    // ── COLUMN HEADERS ──────────────────────────────────────
    const headers = [
      { lbl: 'External Entities',     x: -650, color: RED    },
      { lbl: 'Workfront Fusion',      x:    0, color: BLUE   },
      { lbl: 'Adobe I/O Runtime',     x:  420, color: PURPLE },
      { lbl: 'Workfront Planning',    x:  820, color: GREEN  },
    ];
    for (const h of headers) {
      console.log(`  header: ${h.lbl}`);
      await b.createText({
        content: h.lbl,
        x: h.x - 100, y: -630, width: 200,
        style: { textAlign: 'center', fontSize: 13, color: h.color },
      });
    }

    // ── ADOBE I/O RUNTIME — background container ─────────────
    await S('io_bg', {
      type: 'shape', shape: 'rectangle',
      content: '',
      x: 420, y: 180, width: 310, height: 1210,
      style: {
        fillColor : '#F5F0FF',
        borderColor: PURPLE,
        borderWidth: 2,
        borderStyle: 'dashed',
        textAlign : 'center',
        textAlignVertical: 'middle',
        fontSize  : 12,
        color     : PURPLE,
      },
    });

    // ── SFDC NOTE ────────────────────────────────────────────
    await S('sfdc', {
      type: 'shape', shape: 'rectangle',
      content: 'SFDC Values\ns_rtid / s_iid in CTA URL fields\nNo Salesforce API call',
      x: L.sfdc.x, y: L.sfdc.y, width: 210, height: 78,
      style: sd('#FFFDE7', ORANGE, '#5C4B00', 10),
    });

    // ── EXTERNAL ENTITIES ────────────────────────────────────
    await S('marketer', {
      type: 'shape', shape: 'rectangle',
      content: 'Marketer\nAPAC / AMER / EMEA',
      x: L.marketer.x, y: L.marketer.y, width: 185, height: 72,
      style: ss('#FFF0EF', RED, 3, RED, 13),
    });
    await S('opsTeam', {
      type: 'shape', shape: 'rectangle',
      content: 'Operations Team\nMCZ Review & QA',
      x: L.opsTeam.x, y: L.opsTeam.y, width: 185, height: 72,
      style: ss('#E8F1FC', BLUE, 3, BLUE, 13),
    });
    await S('marketo', {
      type: 'shape', shape: 'rectangle',
      content: 'Adobe Marketo\nMCZ Programs',
      x: L.marketo.x, y: L.marketo.y, width: 185, height: 72,
      style: ss('#FEF3E2', ORANGE, 3, ORANGE, 13),
    });

    // ── FUSION PROCESSES ─────────────────────────────────────
    const procs = [
      { key:'p1', c:RED,    txt:'P1  Intake Processing\nS1 · Validate & Route'          },
      { key:'p2', c:BLUE,   txt:'P2  Project Scaffolding\nS2 · Marketer Project Create'  },
      { key:'p3', c:BLUE,   txt:'P3  Content Management\nS3 · Watch & Update content.js' },
      { key:'p4', c:GREEN,  txt:'P4  Governance Check\nS4 · Email Approval Gate'         },
      { key:'p5', c:BLUE,   txt:'P5  Ops & Sync Build\nS5+S6 · Prepare MCZ Payload'     },
      { key:'p6', c:ORANGE, txt:'P6  API Dispatch\nS6 · SnapLogic Gateway'               },
      { key:'p7', c:PURPLE, txt:'P7  Response Processing\nS7 · Update & Activate QA'    },
    ];
    for (const p of procs) {
      await S(p.key, {
        type: 'shape', shape: 'rectangle',
        content: p.txt,
        x: L[p.key].x, y: L[p.key].y, width: 248, height: 72,
        style: ss('#FFFFFF', p.c, 3, DARK, 12),
      });
    }

    // ── ADOBE I/O RUNTIME ACTIONS ─────────────────────────────
    const ioActions = [
      { key:'io_validation',    c:PURPLE, txt:'validation-summary\nEvaluates rules by region & severity'     },
      { key:'io_overview',      c:PURPLE, txt:'overview-build\nGenerates readable request overview'          },
      { key:'io_ops_overview',  c:PURPLE, txt:'overview-summary-ops\nGenerates ops-level overview'           },
      { key:'io_sync_build',    c:PURPLE, txt:'sync-object-build\nBuilds MCZ JSON payload from content.js'   },
      { key:'io_response_proc', c:PURPLE, txt:'snaplogic-response-processor\nDecodes provisioning response'  },
    ];
    for (const a of ioActions) {
      await S(a.key, {
        type: 'shape', shape: 'rectangle',
        content: a.txt,
        x: L[a.key].x, y: L[a.key].y, width: 280, height: 72,
        style: ss('#F1ECFE', PURPLE, 2, DARK, 11),
      });
    }

    // ── DATA STORES ──────────────────────────────────────────
    const stores = [
      { key:'d1', txt:'D1  Campaign Request Table\nCore request storage'         },
      { key:'d2', txt:'D2  Lookup Tables (4)\nSolutions · Industry · POI · Team' },
      { key:'d3', txt:'D3  Validation Rules\nRegion-specific compliance'          },
      { key:'d4', txt:'D4  MCZ Taxonomy & Shells\nTokens & program templates'     },
      { key:'d5', txt:'D5  content.js\nVersioned campaign JSON'                  },
    ];
    for (const s of stores) {
      await S(s.key, {
        type: 'shape', shape: 'rectangle',
        content: s.txt,
        x: L[s.key].x, y: L[s.key].y, width: 238, height: 60,
        style: ss('#E6F5F0', GREEN, 2, DARK, 11, 'left'),
      });
    }

    // ── CONNECTORS ───────────────────────────────────────────
    console.log('  building connectors...');
    const R  = { x: 1,   y: 0.5 };
    const LL = { x: 0,   y: 0.5 };
    const T  = { x: 0.5, y: 0   };
    const B  = { x: 0.5, y: 1   };

    // — Intake flow ───────────────────────────────────────────
    await C('sfdc',    'marketer', 'SFDC URL params in CTA fields', { color:ORANGE, dashed:true, sp:B,  ep:T  });
    await C('marketer','p1',       'Campaign request + CTA data',   { color:RED,   thick:true,  sp:R,  ep:LL });
    await C('p1',      'd1',       'Store validated request',        { color:GREEN,              sp:R,  ep:LL });
    await C('d2',      'p1',       'Lookup enrichment',              { color:GREEN, dashed:true, sp:LL, ep:R  });

    // — P1 → Adobe I/O validation ─────────────────────────────
    await C('p1', 'io_validation', 'JSON invoke',         { color:PURPLE, thick:true, sp:R,  ep:LL });
    await C('io_validation', 'd3', 'Read rules',          { color:GREEN,  dashed:true,sp:R,  ep:LL });
    await C('io_validation', 'p1', 'Validation result JSON', { color:PURPLE, dashed:true, sp:LL, ep:R });

    // — P2 → Adobe I/O overview-build ─────────────────────────
    await C('p1',  'p2',          'Validated',            { color:BLUE,  thick:true });
    await C('p2',  'io_overview', 'JSON invoke',          { color:PURPLE,thick:true, sp:R,  ep:LL });
    await C('io_overview', 'p2',  'Overview text JSON',   { color:PURPLE,dashed:true,sp:LL, ep:R  });

    // — P3 content management ─────────────────────────────────
    await C('p2',  'p3',  'Project ready',                { color:BLUE,  thick:true });
    await C('p3',  'd5',  'Update content.js JSON',       { color:GREEN,             sp:R,  ep:LL });

    // — P4 governance ─────────────────────────────────────────
    await C('p3',  'p4',  'Content ready',                { color:BLUE,  thick:true });
    await C('d3',  'p4',  'Validation rules',             { color:GREEN, dashed:true,sp:LL, ep:R  });

    // — P5 → Adobe I/O ops overview + sync build ──────────────
    await C('p4',  'p5',  'Approved',                     { color:GREEN, thick:true });
    await C('opsTeam','p5','MCZ Review + SFDC task values',{ color:BLUE,             sp:R,  ep:LL });
    await C('p5',  'io_ops_overview','JSON invoke',        { color:PURPLE,thick:true,sp:R,  ep:LL });
    await C('io_ops_overview','p5', 'Ops overview JSON',  { color:PURPLE,dashed:true,sp:LL, ep:R  });
    await C('p5',  'io_sync_build',  'JSON invoke',        { color:PURPLE,thick:true,sp:R,  ep:LL });
    await C('io_sync_build','d5',    'Read content.js',   { color:GREEN, dashed:true,sp:R,  ep:LL });
    await C('io_sync_build','d4',    'Read taxonomy/shells',{ color:GREEN,dashed:true,sp:R,  ep:LL });
    await C('io_sync_build','p6',    'Sync object JSON',  { color:PURPLE,thick:true, sp:B,  ep:T  });

    // — P6 API dispatch ───────────────────────────────────────
    await C('p6',  'marketo', 'Provision MCZ program',    { color:ORANGE,thick:true, sp:R,  ep:LL });

    // — P7 → Adobe I/O response processor ─────────────────────
    await C('marketo','p7', 'MCZ Response',               { color:ORANGE,            sp:LL, ep:R  });
    await C('p7', 'io_response_proc','JSON invoke',        { color:PURPLE,thick:true, sp:R,  ep:LL });
    await C('io_response_proc','d1', 'Update status & MCZ links', { color:GREEN,dashed:true,sp:R,ep:LL });
    await C('p7', 'opsTeam',  'QA task activated',         { color:BLUE,             sp:LL, ep:B  });

    // ── DONE ─────────────────────────────────────────────────
    console.log('✅ DFD created! Press Ctrl+Shift+H to fit to screen.');

  } catch (err) {
    console.error('❌ Failed:', err.message || err);
    if (err.stack) console.error(err.stack);
  }

})();
