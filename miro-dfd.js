/**
 * ============================================================
 *  Campaign Orchestration Platform — Data Flow Diagram (DFD)
 *  Miro Board Script  ·  Paste into Chrome DevTools Console
 *  while on your Miro board tab.
 * ============================================================
 *
 *  USAGE:
 *    1. Open your Miro board in Chrome
 *    2. Press F12 → Console tab
 *    3. Paste this entire script and press Enter
 *    4. Wait ~15–20 seconds for all shapes to appear
 *
 *  WHAT IT CREATES:
 *    - Title + Legend
 *    - 3 External Entities  (Marketer, Ops Team, Adobe Marketo)
 *    - 1 SFDC Values note   (dashed amber box — no API call)
 *    - 7 Processes          (P1–P7 mapping to Fusion S1–S7)
 *    - 5 Data Stores        (D1–D5)
 *    - 20 labeled connectors with direction arrows
 * ============================================================
 */

(async () => {

  // ── GUARD ──────────────────────────────────────────────────
  if (typeof miro === 'undefined' || !miro.board) {
    console.error('❌  Miro SDK not found. Make sure you are on a Miro board page (app.miro.com).');
    return;
  }

  console.log('🚀  Building DFD on Miro board — please wait...');

  try {
    const b = miro.board;
    const n = {}; // shape id registry: key → id

    // ── HELPERS ────────────────────────────────────────────────

    /** Create a shape, register its id under `key`. */
    const mkShape = async (key, opts) => {
      const s = await b.createShape(opts);
      if (key) n[key] = s.id;
      return s;
    };

    /** Create a labeled, directed connector between two registered shapes. */
    const mkConn = async (fromKey, toKey, label = '', opts = {}) => {
      await b.createConnector({
        shape: 'elbowed',
        style: {
          startStrokeCap : 'none',
          endStrokeCap   : 'arrow',
          strokeColor    : opts.color  || '#666666',
          strokeWidth    : opts.thick  ? 3 : 2,
          strokeStyle    : opts.dashed ? 'dashed' : 'normal',
          fontSize       : 10,
          color          : opts.color  || '#555555',
          fontFamily     : 'open_sans',
        },
        start: { item: n[fromKey], position: opts.sp || { x: 0.5, y: 1 } },
        end  : { item: n[toKey],   position: opts.ep || { x: 0.5, y: 0 } },
        captions: label ? [{ content: label, position: 0.5 }] : [],
      });
    };

    // ── COLOR PALETTE ──────────────────────────────────────────
    const RED    = '#FA0F00';
    const BLUE   = '#1473E6';
    const GREEN  = '#12805C';
    const PURPLE = '#7C3AED';
    const ORANGE = '#E68619';

    // ── LAYOUT (x, y = centre of each element) ─────────────────
    //  Processes form a vertical spine at x=0.
    //  Data stores stack on the right at x=680.
    //  Entities sit on the far left / right.
    //  SFDC note sits top-right.

    const L = {
      // External entities
      marketer : { x: -650, y: -400 },
      opsTeam  : { x: -650, y:  320 },
      marketo  : { x:  860, y:  320 },
      // SFDC note
      sfdc     : { x:  680, y: -560 },
      // Processes
      p1: { x:  0, y: -400 },
      p2: { x:  0, y: -220 },
      p3: { x:  0, y:  -40 },
      p4: { x:  0, y:  140 },
      p5: { x:  0, y:  320 },
      p6: { x: 380, y:  320 },
      p7: { x: 380, y:  500 },
      // Data stores
      d1: { x: 680, y: -340 },
      d2: { x: 680, y: -255 },
      d3: { x: 680, y: -170 },
      d4: { x: 680, y:  -85 },
      d5: { x: 680, y:    0 },
    };

    // ── TITLE ─────────────────────────────────────────────────
    await b.createText({
      content : '<strong>Campaign Orchestration Platform — Data Flow Diagram (DFD)</strong>',
      x: 50, y: -680,
      width: 900,
      style: {
        textAlign  : 'center',
        fontSize   : 22,
        color      : '#2C2C2C',
        fontFamily : 'open_sans',
      },
    });
    await b.createText({
      content : 'Level-1 DFD  ·  APAC / AMER scope  ·  Adobe Campaign Orchestration',
      x: 50, y: -645,
      width: 900,
      style: {
        textAlign  : 'center',
        fontSize   : 13,
        color      : '#888888',
        fontFamily : 'open_sans',
      },
    });

    // ── LEGEND ─────────────────────────────────────────────────
    const legendDefs = [
      { label: 'External Entity',  fill: '#FFF0EF', border: RED    },
      { label: 'Process  (Pn)',    fill: '#EAF2FF', border: BLUE   },
      { label: 'Data Store  (Dn)', fill: '#E6F5F0', border: GREEN  },
      { label: 'SFDC Note',        fill: '#FFFDE7', border: ORANGE },
    ];
    let lx = -680;
    for (const leg of legendDefs) {
      await b.createShape({
        type: 'shape', shape: 'rectangle',
        content: leg.label,
        x: lx, y: -610,
        width: 155, height: 38,
        style: {
          fillColor           : leg.fill,
          borderColor         : leg.border,
          borderWidth         : 2,
          borderStyle         : 'normal',
          borderOpacity       : 1,
          fillOpacity         : 1,
          textAlign           : 'center',
          textAlignVertical   : 'middle',
          fontFamily          : 'open_sans',
          fontSize            : 11,
          color               : '#1A1A1A',
        },
      });
      lx += 170;
    }

    // ── EXTERNAL ENTITIES ──────────────────────────────────────
    const entityBase = {
      type  : 'shape',
      shape : 'rectangle',
      width : 185,
      height: 72,
    };

    await mkShape('marketer', {
      ...entityBase,
      content: 'Marketer\nAPAC / AMER / EMEA',
      x: L.marketer.x, y: L.marketer.y,
      style: {
        fillColor: '#FFF0EF', borderColor: RED, borderWidth: 3,
        borderStyle: 'normal', borderOpacity: 1, fillOpacity: 1,
        textAlign: 'center', textAlignVertical: 'middle',
        fontFamily: 'open_sans', fontSize: 13, color: RED,
      },
    });

    await mkShape('opsTeam', {
      ...entityBase,
      content: 'Operations Team\nMCZ Review & QA',
      x: L.opsTeam.x, y: L.opsTeam.y,
      style: {
        fillColor: '#E8F1FC', borderColor: BLUE, borderWidth: 3,
        borderStyle: 'normal', borderOpacity: 1, fillOpacity: 1,
        textAlign: 'center', textAlignVertical: 'middle',
        fontFamily: 'open_sans', fontSize: 13, color: BLUE,
      },
    });

    await mkShape('marketo', {
      ...entityBase,
      content: 'Adobe Marketo\nMCZ Programs',
      x: L.marketo.x, y: L.marketo.y,
      style: {
        fillColor: '#FEF3E2', borderColor: ORANGE, borderWidth: 3,
        borderStyle: 'normal', borderOpacity: 1, fillOpacity: 1,
        textAlign: 'center', textAlignVertical: 'middle',
        fontFamily: 'open_sans', fontSize: 13, color: ORANGE,
      },
    });

    // ── SFDC NOTE (dashed amber box) ───────────────────────────
    await mkShape('sfdc', {
      type: 'shape', shape: 'rectangle',
      content: 'SFDC Values\nMarketer enters s_rtid / s_iid\nin CTA URL fields — no API call',
      x: L.sfdc.x, y: L.sfdc.y,
      width: 215, height: 82,
      style: {
        fillColor: '#FFFDE7', borderColor: ORANGE, borderWidth: 1,
        borderStyle: 'dashed', borderOpacity: 1, fillOpacity: 1,
        textAlign: 'center', textAlignVertical: 'middle',
        fontFamily: 'open_sans', fontSize: 10, color: '#5C4B00',
      },
    });

    // ── PROCESSES ─────────────────────────────────────────────
    // Each process uses round_rectangle with a coloured left band
    // simulated by the border colour.  Number badge via text label.
    const processDefs = [
      { key: 'p1', color: RED,    label: 'P1  Intake Processing',    sub: 'S1 · Validate & Route' },
      { key: 'p2', color: BLUE,   label: 'P2  Project Scaffolding',  sub: 'S2 · Marketer Project Create' },
      { key: 'p3', color: PURPLE, label: 'P3  Content Management',   sub: 'S3 · Watch & Update content.js' },
      { key: 'p4', color: GREEN,  label: 'P4  Governance Check',     sub: 'S4 · Email Approval Gate' },
      { key: 'p5', color: BLUE,   label: 'P5  Ops & Sync Build',     sub: 'S5+S6 · Build MCZ Payload' },
      { key: 'p6', color: ORANGE, label: 'P6  API Dispatch',         sub: 'SnapLogic Gateway' },
      { key: 'p7', color: PURPLE, label: 'P7  Response Processing',  sub: 'S7 · Update & Activate QA' },
    ];

    for (const p of processDefs) {
      await mkShape(p.key, {
        type: 'shape', shape: 'round_rectangle',
        content: `${p.label}\n${p.sub}`,
        x: L[p.key].x, y: L[p.key].y,
        width: 248, height: 72,
        style: {
          fillColor: '#FFFFFF', borderColor: p.color, borderWidth: 3,
          borderStyle: 'normal', borderOpacity: 1, fillOpacity: 1,
          textAlign: 'center', textAlignVertical: 'middle',
          fontFamily: 'open_sans', fontSize: 12, color: '#1A1A1A',
        },
      });
    }

    // ── DATA STORES ────────────────────────────────────────────
    // Standard DFD open-rectangle notation approximated with
    // a flat rectangle in #E6F5F0 (green tint) + green border.
    const storeDefs = [
      { key: 'd1', label: 'D1  Campaign Request Table',  sub: 'Core request storage' },
      { key: 'd2', label: 'D2  Lookup Tables (4)',       sub: 'Solutions · Industry · POI · Team' },
      { key: 'd3', label: 'D3  Validation Rules',        sub: 'Region-specific compliance' },
      { key: 'd4', label: 'D4  MCZ Taxonomy & Shells',   sub: 'Tokens & program templates' },
      { key: 'd5', label: 'D5  content.js',              sub: 'Versioned campaign JSON' },
    ];

    for (const s of storeDefs) {
      await mkShape(s.key, {
        type: 'shape', shape: 'rectangle',
        content: `${s.label}\n${s.sub}`,
        x: L[s.key].x, y: L[s.key].y,
        width: 238, height: 62,
        style: {
          fillColor: '#E6F5F0', borderColor: GREEN, borderWidth: 2,
          borderStyle: 'normal', borderOpacity: 1, fillOpacity: 1,
          textAlign: 'left', textAlignVertical: 'middle',
          fontFamily: 'open_sans', fontSize: 11, color: '#1A1A1A',
        },
      });
    }

    // ── CONNECTORS ─────────────────────────────────────────────
    // sp = start position on source shape (x,y in 0–1 relative coords)
    // ep = end position on target shape
    // Sides: top={x:0.5,y:0}  bottom={x:0.5,y:1}
    //        left={x:0,y:0.5} right={x:1,y:0.5}

    const R = { x: 1, y: 0.5 };  // right centre
    const LL = { x: 0, y: 0.5 }; // left  centre
    const T  = { x: 0.5, y: 0 }; // top   centre
    const B  = { x: 0.5, y: 1 }; // bottom centre

    // Marketer → P1: campaign request + CTA URL params
    await mkConn('marketer', 'p1',
      'Campaign request + CTA URL params',
      { color: RED, thick: true, sp: R, ep: LL });

    // SFDC note → P1: optional SFDC URL params (dashed)
    await mkConn('sfdc', 'p1',
      'SFDC URL params (optional)',
      { color: ORANGE, dashed: true, sp: B, ep: T });

    // P1 → D1: store validated request
    await mkConn('p1', 'd1',
      'Store request',
      { color: GREEN, sp: R, ep: LL });

    // P1 → P2: validated request
    await mkConn('p1', 'p2',
      'Validated',
      { color: BLUE, thick: true });

    // D2 → P2: lookup enrichment (dashed)
    await mkConn('d2', 'p2',
      'Lookup enrichment',
      { color: GREEN, dashed: true, sp: LL, ep: R });

    // P2 → D5: generate content.js (dashed)
    await mkConn('p2', 'd5',
      'Generate content.js',
      { color: PURPLE, dashed: true, sp: R, ep: LL });

    // P2 → P3: project ready
    await mkConn('p2', 'p3',
      'Project ready',
      { color: BLUE, thick: true });

    // P3 → D5: update JSON
    await mkConn('p3', 'd5',
      'Update JSON',
      { color: PURPLE, sp: R, ep: LL });

    // P3 → P4: content ready
    await mkConn('p3', 'p4',
      'Content ready',
      { color: PURPLE, thick: true });

    // D3 → P4: validation rules (dashed)
    await mkConn('d3', 'p4',
      'Rules',
      { color: GREEN, dashed: true, sp: LL, ep: R });

    // P4 → P5: approved
    await mkConn('p4', 'p5',
      'Approved',
      { color: GREEN, thick: true });

    // Ops Team → P5: MCZ review + SFDC task values
    await mkConn('opsTeam', 'p5',
      'MCZ Review + SFDC task values',
      { color: BLUE, sp: R, ep: LL });

    // D4 → P5: taxonomy + shells (dashed)
    await mkConn('d4', 'p5',
      'Taxonomy + shells',
      { color: GREEN, dashed: true, sp: LL, ep: R });

    // D5 → P5: content.js data (dashed)
    await mkConn('d5', 'p5',
      'content.js data',
      { color: PURPLE, dashed: true, sp: LL, ep: R });

    // P5 → P6: sync object payload
    await mkConn('p5', 'p6',
      'Sync object',
      { color: ORANGE, thick: true, sp: R, ep: LL });

    // P6 → Marketo: provision MCZ program
    await mkConn('p6', 'marketo',
      'Provision MCZ program',
      { color: ORANGE, thick: true, sp: R, ep: LL });

    // Marketo → P7: MCZ response
    await mkConn('marketo', 'p7',
      'MCZ Response',
      { color: ORANGE, sp: B, ep: R });

    // P7 → D1: update status + MCZ links (dashed)
    await mkConn('p7', 'd1',
      'Update status & MCZ links',
      { color: PURPLE, dashed: true, sp: R, ep: R });

    // P7 → Ops Team: QA task activated
    await mkConn('p7', 'opsTeam',
      'QA task activated',
      { color: BLUE, sp: LL, ep: B });

    // ── DONE ──────────────────────────────────────────────────
    console.log('✅  DFD created successfully!');
    console.log('    Tip: Press Ctrl+Shift+H (Fit to screen) to see the full diagram.');

  } catch (err) {
    console.error('❌  Error building DFD:', err.message || err);
    if (err.stack) console.error(err.stack);
  }

})();
