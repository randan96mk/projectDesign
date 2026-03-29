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
 *    4. Watch progress logs — shapes appear in sequence (~20 s)
 *    5. Press Ctrl+Shift+H to fit the full diagram on screen
 * ============================================================
 */

(async () => {

  if (typeof miro === 'undefined' || !miro.board) {
    console.error('❌ Not on a Miro board. Open app.miro.com first.');
    return;
  }

  console.log('🚀 Building DFD — please wait...');
  const b = miro.board;
  const n = {}; // id registry

  // ── SAFE SHAPE STYLE (only fields Miro SDK v2 accepts) ────
  // borderOpacity / fillOpacity omitted — default = 100 (fully opaque)
  // All numeric fields are strict integers.

  const shapeStyle = (fill, border, bw, textColor, fs, align) => ({
    fillColor         : fill,
    borderColor       : border,
    borderWidth       : Math.round(bw),
    borderStyle       : 'normal',
    textAlign         : align || 'center',
    textAlignVertical : 'middle',
    fontSize          : Math.round(fs),
    color             : textColor,
  });

  const dashedStyle = (fill, border, textColor, fs) => ({
    fillColor         : fill,
    borderColor       : border,
    borderWidth       : 1,
    borderStyle       : 'dashed',
    textAlign         : 'center',
    textAlignVertical : 'middle',
    fontSize          : Math.round(fs),
    color             : textColor,
  });

  // ── SHAPE HELPER ──────────────────────────────────────────
  const S = async (key, opts) => {
    console.log(`  Creating: ${key}`);
    const s = await b.createShape(opts);
    n[key] = s.id;
    return s;
  };

  // ── CONNECTOR HELPER ──────────────────────────────────────
  const C = async (from, to, label, opts = {}) => {
    await b.createConnector({
      shape : 'elbowed',
      style : {
        startStrokeCap : 'none',
        endStrokeCap   : 'arrow',
        strokeColor    : opts.color  || '#666666',
        strokeWidth    : opts.thick  ? 3 : 2,
        strokeStyle    : opts.dashed ? 'dashed' : 'normal',
        fontSize       : 10,
        color          : opts.color  || '#555555',
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
  const L = {
    marketer : { x: -650, y: -380 },
    opsTeam  : { x: -650, y:  340 },
    marketo  : { x:  860, y:  340 },
    sfdc     : { x:  680, y: -540 },
    p1: { x:   0, y: -380 },
    p2: { x:   0, y: -200 },
    p3: { x:   0, y:  -20 },
    p4: { x:   0, y:  160 },
    p5: { x:   0, y:  340 },
    p6: { x:  380, y:  340 },
    p7: { x:  380, y:  520 },
    d1: { x:  680, y: -330 },
    d2: { x:  680, y: -250 },
    d3: { x:  680, y: -170 },
    d4: { x:  680, y:  -90 },
    d5: { x:  680, y:   -5 },
  };

  try {

    // ── TITLE ───────────────────────────────────────────────
    console.log('  Creating: title');
    await b.createText({
      content : 'Campaign Orchestration Platform — Data Flow Diagram (DFD)\nLevel-1 DFD  ·  APAC / AMER scope  ·  Adobe Campaign Orchestration',
      x: 50, y: -680, width: 900,
      style: { textAlign: 'center', fontSize: 18, color: DARK },
    });

    // ── LEGEND ──────────────────────────────────────────────
    const legs = [
      { lbl: 'External Entity',  fill: '#FFF0EF', border: RED    },
      { lbl: 'Process (Pn)',     fill: '#EAF2FF', border: BLUE   },
      { lbl: 'Data Store (Dn)', fill: '#E6F5F0', border: GREEN  },
      { lbl: 'SFDC Note',       fill: '#FFFDE7', border: ORANGE },
    ];
    let lx = -680;
    for (const leg of legs) {
      console.log(`  Creating legend: ${leg.lbl}`);
      await b.createShape({
        type: 'shape', shape: 'rectangle',
        content: leg.lbl,
        x: lx, y: -610, width: 158, height: 36,
        style: shapeStyle(leg.fill, leg.border, 2, DARK, 11),
      });
      lx += 172;
    }

    // ── EXTERNAL ENTITIES ────────────────────────────────────
    await S('marketer', {
      type: 'shape', shape: 'rectangle',
      content: 'Marketer\nAPAC / AMER / EMEA',
      x: L.marketer.x, y: L.marketer.y, width: 185, height: 72,
      style: shapeStyle('#FFF0EF', RED, 3, RED, 13),
    });

    await S('opsTeam', {
      type: 'shape', shape: 'rectangle',
      content: 'Operations Team\nMCZ Review & QA',
      x: L.opsTeam.x, y: L.opsTeam.y, width: 185, height: 72,
      style: shapeStyle('#E8F1FC', BLUE, 3, BLUE, 13),
    });

    await S('marketo', {
      type: 'shape', shape: 'rectangle',
      content: 'Adobe Marketo\nMCZ Programs',
      x: L.marketo.x, y: L.marketo.y, width: 185, height: 72,
      style: shapeStyle('#FEF3E2', ORANGE, 3, ORANGE, 13),
    });

    // ── SFDC NOTE ────────────────────────────────────────────
    await S('sfdc', {
      type: 'shape', shape: 'rectangle',
      content: 'SFDC Values\nMarketer enters s_rtid / s_iid in CTA URL fields\nNo Salesforce API call',
      x: L.sfdc.x, y: L.sfdc.y, width: 218, height: 80,
      style: dashedStyle('#FFFDE7', ORANGE, '#5C4B00', 10),
    });

    // ── PROCESSES ────────────────────────────────────────────
    const procs = [
      { key: 'p1', c: RED,    txt: 'P1  Intake Processing\nS1 · Validate & Route'         },
      { key: 'p2', c: BLUE,   txt: 'P2  Project Scaffolding\nS2 · Marketer Project Create' },
      { key: 'p3', c: PURPLE, txt: 'P3  Content Management\nS3 · Watch & Update content.js'},
      { key: 'p4', c: GREEN,  txt: 'P4  Governance Check\nS4 · Email Approval Gate'        },
      { key: 'p5', c: BLUE,   txt: 'P5  Ops & Sync Build\nS5+S6 · Build MCZ Payload'       },
      { key: 'p6', c: ORANGE, txt: 'P6  API Dispatch\nSnapLogic Gateway'                  },
      { key: 'p7', c: PURPLE, txt: 'P7  Response Processing\nS7 · Update & Activate QA'   },
    ];
    for (const p of procs) {
      await S(p.key, {
        type: 'shape', shape: 'rectangle',
        content: p.txt,
        x: L[p.key].x, y: L[p.key].y, width: 248, height: 72,
        style: shapeStyle('#FFFFFF', p.c, 3, DARK, 12),
      });
    }

    // ── DATA STORES ──────────────────────────────────────────
    const stores = [
      { key: 'd1', txt: 'D1  Campaign Request Table\nCore request storage'          },
      { key: 'd2', txt: 'D2  Lookup Tables (4)\nSolutions · Industry · POI · Team'  },
      { key: 'd3', txt: 'D3  Validation Rules\nRegion-specific compliance'           },
      { key: 'd4', txt: 'D4  MCZ Taxonomy & Shells\nTokens & program templates'      },
      { key: 'd5', txt: 'D5  content.js\nVersioned campaign JSON'                   },
    ];
    for (const s of stores) {
      await S(s.key, {
        type: 'shape', shape: 'rectangle',
        content: s.txt,
        x: L[s.key].x, y: L[s.key].y, width: 238, height: 60,
        style: shapeStyle('#E6F5F0', GREEN, 2, DARK, 11, 'left'),
      });
    }

    // ── CONNECTORS ───────────────────────────────────────────
    console.log('  Creating connectors...');
    const R  = { x: 1,   y: 0.5 };
    const LL = { x: 0,   y: 0.5 };
    const T  = { x: 0.5, y: 0   };
    const B  = { x: 0.5, y: 1   };

    await C('marketer','p1',  'Campaign request + CTA URL params', { color:RED,    thick:true, sp:R,  ep:LL });
    await C('sfdc',    'p1',  'SFDC URL params (optional)',         { color:ORANGE, dashed:true,sp:B,  ep:T  });
    await C('p1',      'd1',  'Store request',                      { color:GREEN,              sp:R,  ep:LL });
    await C('p1',      'p2',  'Validated',                          { color:BLUE,   thick:true              });
    await C('d2',      'p2',  'Lookup enrichment',                  { color:GREEN,  dashed:true,sp:LL, ep:R  });
    await C('p2',      'd5',  'Generate content.js',                { color:PURPLE, dashed:true,sp:R,  ep:LL });
    await C('p2',      'p3',  'Project ready',                      { color:BLUE,   thick:true              });
    await C('p3',      'd5',  'Update JSON',                        { color:PURPLE,             sp:R,  ep:LL });
    await C('p3',      'p4',  'Content ready',                      { color:PURPLE, thick:true              });
    await C('d3',      'p4',  'Rules',                              { color:GREEN,  dashed:true,sp:LL, ep:R  });
    await C('p4',      'p5',  'Approved',                           { color:GREEN,  thick:true              });
    await C('opsTeam', 'p5',  'MCZ Review + SFDC task values',      { color:BLUE,               sp:R,  ep:LL });
    await C('d4',      'p5',  'Taxonomy + shells',                  { color:GREEN,  dashed:true,sp:LL, ep:R  });
    await C('d5',      'p5',  'content.js data',                    { color:PURPLE, dashed:true,sp:LL, ep:R  });
    await C('p5',      'p6',  'Sync object',                        { color:ORANGE, thick:true, sp:R,  ep:LL });
    await C('p6',      'marketo','Provision MCZ program',           { color:ORANGE, thick:true, sp:R,  ep:LL });
    await C('marketo', 'p7',  'MCZ Response',                       { color:ORANGE,             sp:B,  ep:R  });
    await C('p7',      'd1',  'Update status & MCZ links',          { color:PURPLE, dashed:true,sp:R,  ep:R  });
    await C('p7',      'opsTeam','QA task activated',               { color:BLUE,               sp:LL, ep:B  });

    console.log('✅ DFD created! Press Ctrl+Shift+H to fit to screen.');

  } catch (err) {
    console.error('❌ Failed:', err.message || err);
  }

})();
