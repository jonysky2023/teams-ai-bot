<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Examen DEX - Operaciones</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tabler-icons/2.44.0/iconfont/tabler-icons.min.css" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #1a1a1a; }
  .app { display: flex; flex-direction: column; height: 100vh; background: #1a1a1a; font-size: 13px; position: relative; overflow: hidden; }
  .app-body { flex: 1; display: flex; overflow: hidden; }
  .sidebar { width: 190px; background: #111; color: #ccc; display: flex; flex-direction: column; flex-shrink: 0; overflow-y: auto; }
  .sidebar-logo { padding: 14px 16px; border-bottom: 0.5px solid #2a2a2a; display: flex; align-items: center; }
  .logo-text { font-size: 18px; font-weight: 700; color: #fff; letter-spacing: -0.5px; }
  .logo-x { color: #f5813e; }
  .sidebar-nav { flex: 1; padding: 8px 0; }
  .nav-item { display: flex; align-items: center; gap: 8px; padding: 8px 16px; cursor: pointer; color: #aaa; font-size: 13px; border-left: 2px solid transparent; justify-content: space-between; }
  .nav-item-main { display: flex; align-items: center; gap: 8px; }
  .nav-item:hover { color: #fff; background: #1e1e1e; }
  .nav-item.active { color: #f5813e; border-left-color: #f5813e; background: #1e1e1e; }
  .nav-item i { font-size: 16px; }
  .nav-item .chev { font-size: 12px; }
  .submenu { display: none; }
  .submenu.open { display: block; }
  .subnav-item { padding: 6px 16px 6px 42px; cursor: pointer; color: #999; font-size: 12px; }
  .subnav-item:hover { color: #fff; background: #1e1e1e; }
  .subnav-item.active { color: #f5813e; background: #1e1e1e; }

  .main { flex: 1; background: #f5f4f0; display: flex; flex-direction: column; overflow: hidden; }
  .topbar { background: #1a1a1a; padding: 8px 20px; display: flex; align-items: center; justify-content: flex-end; gap: 12px; border-bottom: 0.5px solid #2a2a2a; flex-shrink: 0; }
  .tenant-badge { background: #2a2a2a; border-radius: 6px; padding: 4px 10px; display: flex; align-items: center; gap: 6px; color: #ccc; font-size: 12px; }
  .tenant-dot { width: 8px; height: 8px; border-radius: 50%; background: #f5813e; }
  .user-badge { background: #2563eb; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 11px; font-weight: 600; }

  .timer-pill { display: flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; border: 1.5px solid #16a34a; color: #16a34a; background: #f0fdf4; transition: all .3s; }
  .timer-pill.warn { border-color: #d97706; color: #d97706; background: #fffbeb; }
  .timer-pill.danger { border-color: #c0392b; color: #c0392b; background: #fef2f2; }
  .timer-pill i { font-size: 15px; }

  .content { flex: 1; overflow: hidden; display: flex; flex-direction: column; }
  .page { flex: 1; overflow-y: auto; display: flex; flex-direction: column; }
  .page-header { padding: 16px 20px 0; flex-shrink: 0; }

  .enunciado-box { background: #fff; border: 0.5px solid #e0dfd8; border-left: 3px solid #f5813e; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px; font-size: 13px; color: #333; line-height: 1.5; }

  .toolbar { padding: 8px 20px; display: flex; align-items: center; gap: 8px; border-bottom: 0.5px solid #e0dfd8; background: #f5f4f0; flex-shrink: 0; }
  .btn-tool { display: flex; align-items: center; gap: 4px; padding: 4px 10px; border: 0.5px solid #ccc; border-radius: 6px; background: #fff; color: #444; font-size: 12px; cursor: pointer; }
  .btn-tool:hover { background: #f0efe8; }
  .btn-tool i { font-size: 14px; }
  .filter-chip { display: flex; align-items: center; gap: 4px; padding: 4px 10px; border: 0.5px solid #d4a96a; border-radius: 6px; background: #fdf6ec; color: #7a5a2a; font-size: 12px; cursor: pointer; }
  .filter-chip b { color: #c87d30; }
  .search-box { display: flex; align-items: center; gap: 6px; border: 0.5px solid #ccc; border-radius: 6px; padding: 4px 10px; background: #fff; flex: 1; max-width: 220px; }
  .search-box input { border: none; outline: none; font-size: 12px; color: #333; background: transparent; width: 100%; }
  .search-box i { font-size: 14px; color: #999; }

  .table-wrap { flex: 1; overflow-y: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  thead tr { background: #eceae3; }
  th { padding: 7px 14px; text-align: left; color: #555; font-weight: 500; border-bottom: 0.5px solid #ddd; white-space: nowrap; }
  td { padding: 8px 14px; border-bottom: 0.5px solid #eee; color: #333; }
  tr.clickable { cursor: pointer; }
  tr.clickable:hover td { background: #f0efe8; }
  .status-ok { color: #1a7a3a; font-weight: 500; }
  .status-err { color: #c0392b; font-weight: 500; }
  .status-warn { color: #c87d30; font-weight: 500; }
  .status-crit { color: #c0392b; font-weight: 500; }
  .desc-link { color: #2563eb; text-decoration: none; }

  .detail-layout { flex: 1; display: flex; overflow: hidden; }
  .detail-sidebar { width: 170px; background: #fff; border-right: 0.5px solid #e0dfd8; padding: 12px 0; flex-shrink: 0; }
  .detail-section-title { font-size: 11px; color: #999; padding: 4px 16px 6px; text-transform: uppercase; letter-spacing: .05em; }
  .detail-nav-item { padding: 7px 16px; cursor: pointer; font-size: 12px; color: #555; display: flex; align-items: center; justify-content: space-between; border-left: 2px solid transparent; }
  .detail-nav-item:hover { background: #f5f4f0; color: #222; }
  .detail-nav-item.active { color: #2563eb; border-left-color: #2563eb; background: #eff6ff; }
  .detail-nav-count { background: #e0dfd8; border-radius: 10px; padding: 1px 6px; font-size: 11px; color: #666; }
  .detail-nav-count.blue { background: #dbeafe; color: #2563eb; }

  .events-panel { flex: 1; overflow: hidden; display: flex; flex-direction: column; padding: 12px 18px; }
  .events-toolbar { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; flex-shrink: 0; }
  .events-table-wrap { flex: 1; overflow-y: auto; }
  .events-table { width: 100%; border-collapse: collapse; font-size: 12px; }
  .events-table th { padding: 6px 10px; text-align: left; color: #666; font-weight: 500; border-bottom: 0.5px solid #ddd; }
  .events-table td { padding: 0; border-bottom: 0.5px solid #eee; vertical-align: top; }
  .event-row-main { display: flex; align-items: flex-start; cursor: pointer; }
  .event-row-main:hover { background: #f5f4f0; }
  .event-col { padding: 8px 10px; }
  .event-output { display: none; background: #fafaf8; border-top: 0.5px solid #eee; padding: 10px 14px 10px 32px; }
  .event-output.open { display: block; }
  .output-text { font-family: "SFMono-Regular", Consolas, monospace; font-size: 11px; color: #333; line-height: 1.7; white-space: pre-wrap; }
  .type-info { color: #2563eb; font-size: 12px; }

  .pager { padding: 8px 18px; display: flex; align-items: center; justify-content: space-between; border-top: 0.5px solid #e0dfd8; font-size: 12px; color: #777; background: #f5f4f0; flex-shrink: 0; }
  .pager-btn { padding: 3px 7px; border: 0.5px solid #ccc; border-radius: 4px; background: #fff; cursor: pointer; color: #555; font-size: 11px; }
  .pager-btn:disabled { opacity: .4; cursor: default; }

  .breadcrumb { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #888; margin-bottom: 8px; }
  .breadcrumb a { color: #2563eb; cursor: pointer; text-decoration: none; }
  .breadcrumb a:hover { text-decoration: underline; }

  /* Barra de respuesta global, fija en la parte inferior, visible en cualquier pantalla */
  .answer-bar { flex-shrink: 0; background: #1a1a1a; border-top: 1px solid #2a2a2a; padding: 10px 20px; display: flex; align-items: center; gap: 12px; }
  .answer-bar-label { color: #ccc; font-size: 12px; white-space: nowrap; }
  .answer-bar input { border: 0.5px solid #444; border-radius: 6px; padding: 7px 12px; font-size: 13px; width: 200px; outline: none; background: #262626; color: #fff; }
  .answer-bar input:focus { border-color: #f5813e; }
  .answer-bar input:disabled { background: #333; color: #777; cursor: not-allowed; }
  .answer-bar-submit { background: #f5813e; color: #fff; border: none; border-radius: 6px; padding: 7px 18px; font-size: 13px; font-weight: 500; cursor: pointer; }
  .answer-bar-submit:hover:not(:disabled) { background: #e06b28; }
  .answer-bar-submit:disabled { background: #555; cursor: not-allowed; color: #999; }
  .answer-bar-msg { font-size: 12px; color: #999; margin-left: auto; }

  .overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,.55); align-items: center; justify-content: center; z-index: 100; }
  .overlay.open { display: flex; }
  .modal { background: #fff; border-radius: 12px; padding: 32px 40px; text-align: center; min-width: 300px; max-width: 380px; }
  .modal-icon { font-size: 40px; margin-bottom: 12px; color: #16a34a; }
  .modal-title { font-size: 18px; font-weight: 600; color: #1a1a1a; margin-bottom: 8px; }
  .modal-sub { font-size: 13px; color: #666; line-height: 1.5; }

  /* Detalle de Grupo de Workspaces */
  .gws-tabs { display: flex; gap: 4px; border-bottom: 0.5px solid #e0dfd8; margin-top: 10px; }
  .gws-tab { padding: 8px 14px; font-size: 13px; color: #666; cursor: pointer; border-bottom: 2px solid transparent; }
  .gws-tab:hover { color: #222; }
  .gws-tab.active { color: #1a1a1a; font-weight: 600; border-bottom-color: #f5813e; }
  .gws-panel { padding: 16px 0; }
  .gws-card { background: #fff; border: 0.5px solid #e0dfd8; border-radius: 8px; padding: 20px; }
  .gws-field-label { font-size: 11px; color: #999; margin-bottom: 2px; }
  .gws-field-value { font-size: 14px; color: #222; margin-bottom: 16px; }
  .gws-side-box { background: #fff; border: 0.5px solid #e0dfd8; border-radius: 8px; padding: 14px 16px; display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
  .gws-side-box i { font-size: 20px; color: #f5813e; }
  .gws-side-label { font-size: 11px; color: #999; }
  .gws-side-value { font-size: 14px; font-weight: 600; color: #222; }
  .gws-empty { text-align: center; padding: 60px 20px; color: #888; }
  .gws-empty i { font-size: 40px; color: #ccc; margin-bottom: 10px; display: block; }

  .bar-chart-wrap { display: flex; align-items: flex-end; gap: 6px; height: 180px; padding: 10px 0; border-bottom: 1px solid #ddd; }
  .bar-chart-bar { background: #f5813e; width: 100%; border-radius: 2px 2px 0 0; }
  .bar-chart-labels { display: flex; gap: 6px; margin-top: 6px; }
  .bar-chart-labels span { width: 100%; font-size: 10px; color: #888; text-align: center; white-space: nowrap; }

  /* Panel lateral de "Nueva acción programada" */
  .side-panel-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,.4); z-index: 200; justify-content: flex-end; }
  .side-panel-overlay.open { display: flex; }
  .side-panel { background: #fff; width: 420px; max-width: 92vw; height: 100%; overflow-y: auto; padding: 20px 24px; box-shadow: -4px 0 16px rgba(0,0,0,.15); }
  .side-panel-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 0.5px solid #e0dfd8; padding-bottom: 12px; margin-bottom: 16px; }
  .side-panel-title { font-size: 17px; font-weight: 600; color: #1a1a1a; }
  .side-panel-close { background: none; border: none; font-size: 20px; color: #888; cursor: pointer; }
  .sp-label { font-size: 13px; font-weight: 500; color: #333; margin: 16px 0 6px; }
  .sp-label .req { color: #c0392b; }
  .sp-select, .sp-input { width: 100%; border: 0.5px solid #ccc; border-radius: 6px; padding: 8px 10px; font-size: 13px; color: #333; outline: none; }
  .sp-select:focus, .sp-input:focus { border-color: #2563eb; }
  .sp-input.err { border-color: #c0392b; }
  .sp-err-msg { font-size: 11px; color: #c0392b; margin-top: 4px; }
  .sp-box { border: 0.5px solid #e0dfd8; border-radius: 8px; padding: 14px; margin-top: 6px; }
  .sp-radio-row { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #333; margin-bottom: 10px; }
  .sp-days-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 20px; padding-left: 22px; }
  .sp-day-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #333; }
  .sp-footer { display: flex; justify-content: flex-end; gap: 10px; margin-top: 24px; border-top: 0.5px solid #e0dfd8; padding-top: 16px; }
  .sp-btn { border-radius: 6px; padding: 8px 18px; font-size: 13px; font-weight: 500; cursor: pointer; border: none; }
  .sp-btn-cancel { background: #fff; border: 0.5px solid #ccc; color: #555; }
  .sp-btn-submit { background: #f5813e; color: #fff; }

  #token-box { font-family: "SFMono-Regular", Consolas, monospace; font-size: 17px; font-weight: 700; letter-spacing: 1px; background: #f5f4f0; border: 1.5px dashed #f5813e; border-radius: 8px; padding: 12px 16px; margin-top: 10px; color: #1a1a1a; user-select: all; }
  #copy-token-btn { margin-top: 10px; }

  .home-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin: 16px 0; }
  .home-card { background: #fff; border: 0.5px solid #e0dfd8; border-radius: 10px; padding: 24px; text-align: center; cursor: pointer; }
  .home-card:hover { border-color: #ccc; }
  .home-card i { font-size: 32px; color: #f5813e; margin-bottom: 10px; display: block; }
  .home-card-title { font-size: 14px; font-weight: 500; color: #333; }
  .home-tag { display: inline-block; background: #1a1a1a; color: #fff; font-size: 11px; padding: 2px 8px; border-radius: 4px; margin-left: 8px; }
  .ver-mas { padding: 10px 0; color: #555; font-size: 13px; display: flex; align-items: center; gap: 6px; border-bottom: 0.5px solid #e0dfd8; margin-bottom: 8px; cursor: pointer; }
  .productos-title { font-size: 15px; font-weight: 500; color: #333; margin: 12px 0 8px; }

  .ia-box { border: 0.5px solid #ccc; border-radius: 8px; padding: 14px; margin-bottom: 14px; background: #fff; }
  .ia-hint { background: #f5f4f0; border-radius: 6px; padding: 8px 12px; font-size: 12px; color: #555; margin-bottom: 12px; display: flex; gap: 6px; align-items: center; }
  .ia-hint i { color: #888; }
  .ia-input { border: 0.5px solid #ccc; border-radius: 6px; padding: 10px 12px; width: 100%; font-size: 13px; color: #333; min-height: 20px; }
  .ia-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 14px; margin-top: 14px; }
  .ia-cat { border: 0.5px solid #e0dfd8; border-radius: 8px; padding: 12px; background: #fff; }
  .ia-cat-title { font-size: 12px; font-weight: 500; color: #333; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
  .ia-cat-title i { color: #f5813e; }
  .ia-q { border: 0.5px solid #e0dfd8; border-radius: 6px; padding: 7px 10px; font-size: 11px; color: #555; margin-bottom: 6px; cursor: pointer; }
  .ia-q:hover { background: #f5f4f0; }

  .report-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 16px; margin-top: 14px; }
  .report-card { background: #fff; border: 0.5px solid #e0dfd8; border-radius: 10px; padding: 20px; text-align: center; }
  .report-card-title { font-size: 14px; font-weight: 500; color: #333; margin-bottom: 4px; }
  .report-card-sub { font-size: 11px; color: #888; margin-bottom: 4px; }
  .report-shared { font-size: 11px; color: #1a7a3a; display: flex; align-items: center; gap: 4px; justify-content: center; margin-bottom: 14px; }
  .report-btn { border: 0.5px solid #ccc; border-radius: 6px; padding: 5px 14px; font-size: 12px; background: #fff; cursor: pointer; }
</style>
</head>
<body>

<div class="app" id="app">

  <div class="app-body">
    <div class="sidebar">
      <div class="sidebar-logo"><div class="logo-text">fle<span class="logo-x">xx</span>ible</div></div>
      <nav class="sidebar-nav" id="sidebar-nav">
        <div class="nav-item" data-page="inicio"><div class="nav-item-main"><i class="ti ti-home"></i> Inicio</div></div>
        <div class="nav-item" data-page="operaciones"><div class="nav-item-main"><i class="ti ti-activity"></i> Operaciones</div></div>
        <div class="nav-item" data-page="flujos"><div class="nav-item-main"><i class="ti ti-arrows-exchange"></i> Flujos</div></div>

        <div class="nav-item" data-toggle="informes"><div class="nav-item-main"><i class="ti ti-chart-bar"></i> Informes</div><i class="ti ti-chevron-down chev"></i></div>
        <div class="submenu" id="sub-informes">
          <div class="subnav-item" data-page="informes">Informes</div>
          <div class="subnav-item" data-page="crearia">Crear con IA</div>
        </div>

        <div class="nav-item" data-toggle="inquilinos"><div class="nav-item-main"><i class="ti ti-users"></i> Inquilinos</div><i class="ti ti-chevron-down chev"></i></div>
        <div class="submenu" id="sub-inquilinos">
          <div class="subnav-item" data-page="inquilinos">Inquilinos</div>
          <div class="subnav-item" data-page="activacion">Activación</div>
        </div>

        <div class="nav-item" data-toggle="monitor"><div class="nav-item-main"><i class="ti ti-shield"></i> Monitor</div><i class="ti ti-chevron-down chev"></i></div>
        <div class="submenu" id="sub-monitor">
          <div class="subnav-item" data-page="alertas">Active alerts</div>
          <div class="subnav-item" data-page="alertconfig">Alerts Settings</div>
        </div>

        <div class="nav-item" data-toggle="workspaces"><div class="nav-item-main"><i class="ti ti-layout-grid"></i> Workspaces</div><i class="ti ti-chevron-down chev"></i></div>
        <div class="submenu" id="sub-workspaces">
          <div class="subnav-item" data-page="workspaces">Workspaces</div>
          <div class="subnav-item" data-page="sesiones">Sesiones</div>
          <div class="subnav-item" data-page="gruposworkspaces">Grupos de workspaces</div>
          <div class="subnav-item" data-page="ubicaciones">Ubicaciones</div>
          <div class="subnav-item" data-page="redes">Redes</div>
          <div class="subnav-item" data-page="notificaciones">Notificaciones</div>
          <div class="subnav-item" data-page="redesinalambricas">Redes inalámbricas</div>
        </div>

        <div class="nav-item" data-toggle="actualizaciones"><div class="nav-item-main"><i class="ti ti-clipboard-list"></i> Actualizaciones</div><i class="ti ti-chevron-down chev"></i></div>
        <div class="submenu" id="sub-actualizaciones">
          <div class="subnav-item" data-page="actresumen">Resumen</div>
          <div class="subnav-item" data-page="actgrupos">Grupos de reporte</div>
          <div class="subnav-item" data-page="actpatches">Microsoft Patches</div>
          <div class="subnav-item" data-page="actdirectivas">Directivas de actualizaciones</div>
          <div class="subnav-item" data-page="actdestinatarios">Destinatarios</div>
        </div>

        <div class="nav-item" data-page="microservicios"><div class="nav-item-main"><i class="ti ti-cpu"></i> Microservicios</div></div>
        <div class="nav-item" data-page="config"><div class="nav-item-main"><i class="ti ti-settings"></i> Configuración</div></div>
      </nav>
    </div>

    <div class="main">
      <div class="topbar">
        <div class="tenant-badge"><div class="tenant-dot"></div><span>Flexxible Training</span></div>
        <div style="font-size:12px;color:#ccc;" id="student-name-label">Alumno</div>
        <div class="user-badge" id="student-initials">--</div>
      </div>
      <div class="content" id="content-area"></div>
    </div>
  </div>

  <div class="side-panel-overlay" id="sp-overlay">
    <div class="side-panel">
      <div class="side-panel-header">
        <div class="side-panel-title">Nueva acción programada</div>
        <button class="side-panel-close" id="sp-close">×</button>
      </div>

      <div class="sp-label">Acción <span class="req">*</span></div>
      <select class="sp-select" id="sp-accion">
        <option value="">Seleccionar una acción</option>
        <option value="wol">Wake On LAN</option>
        <option value="apagar">Apagar</option>
        <option value="reiniciar">Reiniciar</option>
      </select>

      <div class="sp-label">Programación <span class="req">*</span></div>
      <div class="sp-box">
        <div style="font-size:12px;color:#555;margin-bottom:8px;">Hora de inicio:</div>
        <input class="sp-input" type="time" id="sp-hora">
        <div class="sp-err-msg" id="sp-hora-err" style="display:none;">El tiempo es obligatorio</div>

        <div style="border-top:0.5px solid #eee;margin:14px 0;"></div>
        <div style="font-size:12px;color:#555;margin-bottom:8px;">Patrón de recurrencia</div>
        <div class="sp-radio-row"><input type="radio" checked disabled> Semanal</div>
        <div class="sp-days-grid">
          <label class="sp-day-item"><input type="checkbox" value="Lunes"> Lunes</label>
          <label class="sp-day-item"><input type="checkbox" value="Martes"> Martes</label>
          <label class="sp-day-item"><input type="checkbox" value="Miércoles"> Miércoles</label>
          <label class="sp-day-item"><input type="checkbox" value="Jueves"> Jueves</label>
          <label class="sp-day-item"><input type="checkbox" value="Viernes"> Viernes</label>
          <label class="sp-day-item"><input type="checkbox" value="Sábado"> Sábado</label>
          <label class="sp-day-item"><input type="checkbox" value="Domingo"> Domingo</label>
        </div>
      </div>
      <div class="sp-err-msg" id="sp-dias-err" style="display:none;">Selecciona al menos un día</div>

      <div class="sp-label">Zona horaria <span class="req">*</span></div>
      <select class="sp-select" id="sp-zona">
        <option value="">Seleccionar zona horaria</option>
        <option value="madrid">(UTC+01:00) Madrid</option>
        <option value="samoa">(UTC-11:00) Midway Island, Samoa</option>
        <option value="hawaii">(UTC-10:00) Hawaii</option>
        <option value="alaska">(UTC-09:00) Alaska</option>
        <option value="pacific">(UTC-08:00 / UTC-07:00) Pacific Time (US &amp; Canada)</option>
        <option value="tijuana">(UTC-08:00 / UTC-07:00) Tijuana, Baja California</option>
        <option value="arizona">(UTC-07:00) Arizona</option>
        <option value="mountain">(UTC-07:00 / UTC-06:00) Mountain Time (US &amp; Canada)</option>
      </select>
      <div class="sp-err-msg" id="sp-zona-err" style="display:none;">La zona horaria es obligatoria</div>

      <div class="sp-footer">
        <button class="sp-btn sp-btn-cancel" id="sp-cancel">Cancelar</button>
        <button class="sp-btn sp-btn-submit" id="sp-submit">+ Nuevo</button>
      </div>
    </div>
  </div>

  <div class="overlay" id="token-overlay">
    <div class="modal">
      <div class="modal-icon"><i class="ti ti-circle-check"></i></div>
      <div class="modal-title" id="token-title">Programación creada</div>
      <div class="modal-sub" id="token-sub"></div>
      <div id="token-box" style="display:none;"></div>
      <button class="sp-btn sp-btn-submit" id="copy-token-btn" style="display:none;">Copiar código</button>
      <div style="margin-top:16px;"><button class="sp-btn sp-btn-cancel" id="token-close">Cerrar</button></div>
    </div>
  </div>

</div>

<script>
var TOKEN_PROGRAMACION_APAGADO = "FLX-SCHED-APAGADO-OK";
var grupoWSState = { activeTab: 'detalles', programaciones: [] };
var TARGET_OP_ID = 2;

var state = { finished:false, currentPage:'inicio' };

var ENUNCIADO = "";

var ops = [
  {id:0,desc:"Microservice on DESKTOP-DEFE7N5 (Network data usage) requested by 'Automatic alert trigger'",type:"Ejecución de microservicios",el:1,sc:"ok",lbl:"Finalizado"},
  {id:1,desc:"Microservice 'Download and install 7-Zip silently' requested by 'User: Training'",type:"Microservicio de usuario final",el:1,sc:"err",lbl:"Error"},
  {id:2,desc:"Microservice on DESKTOP-DEFE7N5 (Detect HDMI and other display connections (1)) requested by 'jserra@flexxible.com'",type:"Ejecución de microservicios",el:1,sc:"ok",lbl:"Finalizado"},
  {id:3,desc:"Request Remote Assistance session for user 'DESKTOP-DEFE7N5 Training' on VM 'DESKTOP-DEFE7N5'",type:"Asistencia remota",el:1,sc:"ok",lbl:"Finalizado"},
  {id:4,desc:"Process scheduled WakeOnLAN for Workspace group: 698c5f7c94be46ccaec3a2cb with name RAM",type:"Wake on LAN",el:1,sc:"ok",lbl:"Finalizado"},
  {id:5,desc:"Generate Notifications - Target: Workspace - Total created notifications: 1",type:"Enviar notificación",el:1,sc:"ok",lbl:"Finalizado"},
  {id:6,desc:"Microservice on DESKTOP-DEFE7N5 (Detect HDMI and other display connections (1)) requested by 'jserra@flexxible.com'",type:"Ejecución de microservicios",el:1,sc:"ok",lbl:"Finalizado"},
  {id:7,desc:"Microservice on DESKTOP-DEFE7N5 (Download and install 7-Zip silently) requested by 'User: Training'",type:"Microservicio de usuario final",el:1,sc:"ok",lbl:"Finalizado"},
  {id:8,desc:"Process scheduled WakeOnLAN for Workspace group: 698c5f7c94be46ccaec3a2cb with name RAM",type:"Wake on LAN",el:1,sc:"ok",lbl:"Finalizado"},
  {id:9,desc:"Microservice on DESKTOP-DEFE7N5 (Empty the recycle bin for all users) requested by 'API LAB TRAINING'",type:"Ejecución de microservicios",el:1,sc:"warn",lbl:"Tiempo de espera agotado"}
];

var eventData = [
  {date:"27/8/26, 9:52:30",type:"Información",origen:"DESKTOP-DEFE7N5",msg:"Output: === Display Connection Detection === Found 2 monitor(s) connected: -- Monitor 1 -...",
   output:"=== Display Connection Detection ===\n\nFound 2 monitor(s) connected:\n\n--- Monitor 1 ---\nName: Generic PnP Monitor\nDevice ID: DesktopMonitor1\nScreen Height: 768 pixels\nScreen Width: 1024 pixels\nStatus: OK\n\n--- Monitor 2 ---\nName: Generic Non-PnP Monitor\nDevice ID: DesktopMonitor2\nStatus: OK\n\n=== Video Controller Information ===\nName: Microsoft Hyper-V Video\nDriver Version: 10.0.19041.1\nCurrent Resolution: 1024 x 768"},
  {date:"27/8/26, 9:52:23",type:"Información",origen:"DESKTOP-DEFE7N5",msg:"Execution started...",output:"Execution started. The microservice is now running on the target device."},
  {date:"27/8/26, 9:52:16",type:"Información",origen:"DESKTOP-DEFE7N5",msg:"The message has been sent to the device; the message is valid for 30 minutes...",output:"The message has been sent to the device; the message is valid for 30 minutes, and if the message is not processed within this time, it will be discarded."}
];

function fmt(s){ return String(Math.floor(s/60)).padStart(2,'0') + ':' + String(s%60).padStart(2,'0'); }

function enunciadoHtml(){
  if (!ENUNCIADO) return '';
  return '<div class="enunciado-box">' + ENUNCIADO + '</div>';
}

function setActiveNav(page){
  document.querySelectorAll('.nav-item[data-page]').forEach(function(el){ el.classList.toggle('active', el.dataset.page === page); });
  document.querySelectorAll('.subnav-item').forEach(function(el){ el.classList.toggle('active', el.dataset.page === page); });
}

function goPage(page){
  if (state.finished) return;
  state.currentPage = page;
  setActiveNav(page);
  var area = document.getElementById('content-area');

  if (page === 'inicio') area.innerHTML = pageInicio();
  else if (page === 'operaciones'){
    area.innerHTML = pageOperaciones();
    renderOps();
    var opsSearch = document.getElementById('ops-search');
    if (opsSearch) opsSearch.addEventListener('input', function(){ renderOps(opsSearch.value); });
  }
  else if (page === 'opdetail'){ area.innerHTML = pageOpDetail(); }
  else if (page === 'flujos') area.innerHTML = pageFlujos();
  else if (page === 'informes') area.innerHTML = pageInformes();
  else if (page === 'crearia') area.innerHTML = pageCrearIA();
  else if (page === 'inquilinos') area.innerHTML = pageInquilinos();
  else if (page === 'activacion') area.innerHTML = pageActivacion();
  else if (page === 'alertas'){
    area.innerHTML = pageAlertas();
    renderAlertas();
    var alertsSearch = document.getElementById('alerts-search');
    if (alertsSearch) alertsSearch.addEventListener('input', function(){ renderAlertas(alertsSearch.value); });
  }
  else if (page === 'alertconfig') area.innerHTML = pageAlertConfig();
  else if (page === 'workspaces'){
    area.innerHTML = pageWorkspaces();
    renderWorkspaces();
    var wsSearch = document.getElementById('ws-search');
    if (wsSearch) wsSearch.addEventListener('input', function(){ renderWorkspaces(wsSearch.value); });
  }
  else if (page === 'sesiones') area.innerHTML = pageSesiones();
  else if (page === 'gruposworkspaces'){
    area.innerHTML = pageGruposWorkspaces();
    var gwsRow = document.querySelector('tr[data-gws]');
    if (gwsRow) gwsRow.addEventListener('click', function(){ goPage('grupowsdetail'); });
  }
  else if (page === 'grupowsdetail'){ area.innerHTML = pageGrupoWSDetail(); wireGrupoWSTabs(); renderGrupoWSTab('detalles'); }
  else if (page === 'ubicaciones') area.innerHTML = pageUbicaciones();
  else if (page === 'redes') area.innerHTML = pageRedes();
  else if (page === 'notificaciones') area.innerHTML = pageNotificaciones();
  else if (page === 'redesinalambricas'){
    area.innerHTML = pageRedesInalambricas();
    renderRedesInalambricas();
    var wifiSearch = document.getElementById('wifi-search');
    if (wifiSearch) wifiSearch.addEventListener('input', function(){ renderRedesInalambricas(wifiSearch.value); });
  }
  else if (page === 'actresumen') area.innerHTML = pageActResumen();
  else if (page === 'actgrupos') area.innerHTML = pageActGrupos();
  else if (page === 'actpatches') area.innerHTML = pageActPatches();
  else if (page === 'actdirectivas') area.innerHTML = pageActDirectivas();
  else if (page === 'actdestinatarios') area.innerHTML = pageActDestinatarios();
  else area.innerHTML = pageGeneric();
}

function pageInicio(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() +
    '<div style="font-size:18px;font-weight:600;color:#1a1a1a;display:flex;align-items:center;gap:8px;">' +
    '<i class="ti ti-home" style="color:#f5813e;"></i> Inicio <span class="home-tag">Flexxible Training Site</span></div>' +
    '<div class="home-grid">' +
      '<div class="home-card"><i class="ti ti-scan"></i><div class="home-card-title">Analyzer</div></div>' +
      '<div class="home-card"><i class="ti ti-users-group"></i><div class="home-card-title">Monitor</div></div>' +
      '<div class="home-card"><i class="ti ti-hierarchy-2"></i><div class="home-card-title">Documentación</div></div>' +
    '</div>' +
    '<div class="ver-mas"><i class="ti ti-chevron-down"></i> Ver más (4)</div>' +
    '<div class="productos-title">Tus productos</div>' +
    '<table style="width:100%;font-size:12px;"><thead><tr style="border-bottom:0.5px solid #ddd;"><th style="text-align:left;padding:6px 0;color:#666;">Entorno</th><th style="text-align:left;padding:6px 0;color:#666;">Tipo de producto</th><th style="text-align:left;padding:6px 0;color:#666;">Acción</th></tr></thead>' +
    '<tbody><tr><td style="padding:8px 0;color:#2563eb;">Flexxible Training Site</td><td style="padding:8px 0;color:#555;">FlexxClient</td><td style="padding:8px 0;color:#2563eb;">Ver detalle</td></tr></tbody></table>' +
  '</div></div>';
}

function pageOperaciones(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() +
    '<div style="font-size:18px;font-weight:600;color:#1a1a1a;display:flex;align-items:center;gap:8px;margin-bottom:4px;"><i class="ti ti-activity" style="color:#f5813e;"></i> Operaciones</div>' +
    '<div style="font-size:11px;color:#aaa;margin-bottom:8px;">Requiere FlexxAgent 25.12 o posterior</div></div>' +
    '<div class="toolbar"><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div class="btn-tool"><i class="ti ti-refresh"></i> Recargar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input type="text" id="ops-search" placeholder="Buscar por término..."></div><div class="filter-chip">Estado: <b>Cualquiera</b></div><div class="filter-chip">Tipo: <b>Cualquiera</b></div></div>' +
    '<div class="table-wrap"><table><thead><tr><th>Descripción</th><th>Tipo de operación</th><th>Elementos</th><th>Estado</th></tr></thead><tbody id="ops-tbody"></tbody></table></div>' +
    '<div class="pager"><div style="display:flex;gap:4px;"><button class="pager-btn" disabled>«</button><button class="pager-btn" disabled>‹</button><button class="pager-btn" disabled>›</button><button class="pager-btn" disabled>»</button></div><span id="ops-count">Página 1 de 4 · 1 a 50 de 181 resultados</span><span style="font-size:11px;color:#aaa;">Tamaño de página: 50</span></div>' +
  '</div>';
}

function renderOps(filterText){
  var tbody = document.getElementById('ops-tbody');
  if (!tbody) return;
  var q = (filterText || '').trim().toLowerCase();
  var filtered = q === '' ? ops : ops.filter(function(op){
    return op.desc.toLowerCase().indexOf(q) !== -1 ||
           op.type.toLowerCase().indexOf(q) !== -1 ||
           op.lbl.toLowerCase().indexOf(q) !== -1;
  });
  var countEl = document.getElementById('ops-count');
  if (countEl) {
    countEl.textContent = q === ''
      ? 'Página 1 de 4 · 1 a ' + Math.min(50, ops.length) + ' de 181 resultados'
      : filtered.length + ' resultado' + (filtered.length === 1 ? '' : 's') + ' para "' + filterText.trim() + '"';
  }
  tbody.innerHTML = filtered.map(function(op){
    var sc = op.sc === 'ok' ? 'status-ok' : op.sc === 'err' ? 'status-err' : 'status-warn';
    return '<tr class="clickable" data-opid="' + op.id + '"><td><a class="desc-link">' + op.desc + '</a></td><td>' + op.type + '</td><td style="color:#888">' + op.el + '</td><td><span class="' + sc + '">' + op.lbl + '</span></td></tr>';
  }).join('');
  tbody.querySelectorAll('tr[data-opid]').forEach(function(tr){
    tr.addEventListener('click', function(){ openOp(parseInt(tr.dataset.opid, 10)); });
  });
}

function openOp(id){
  var op = ops.filter(function(o){ return o.id === id; })[0];
  goPage('opdetail');
  document.getElementById('detail-breadcrumb').textContent = op.desc;
  renderEvents(id);
}

function pageOpDetail(){
  return '<div class="page"><div class="page-header"><div class="breadcrumb"><a id="back-to-ops">Operaciones</a><i class="ti ti-chevron-right" style="font-size:11px;"></i><span id="detail-breadcrumb" style="color:#555;max-width:420px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"></span></div></div>' +
  '<div class="detail-layout"><div class="detail-sidebar"><div class="detail-section-title">Detalles</div><div class="detail-nav-item">Visión general</div><div class="detail-nav-item">Workspaces <span class="detail-nav-count">1</span></div><div class="detail-nav-item active">Eventos <span class="detail-nav-count blue">3</span></div></div>' +
  '<div class="events-panel"><div class="events-toolbar"><div class="btn-tool"><i class="ti ti-arrows-maximize"></i> Expandir todo</div><div class="btn-tool"><i class="ti ti-arrows-minimize"></i> Contraer todo</div><div style="flex:1"></div><div class="filter-chip">Tipo: <b>Cualquiera</b></div></div>' +
  '<div class="events-table-wrap"><table class="events-table"><thead><tr><th style="width:24px;"></th><th>Fecha</th><th>Tipo</th><th>Origen</th><th>Mensaje</th></tr></thead><tbody id="events-tbody"></tbody></table></div>' +
  '</div></div></div>';
}

function wireOpDetailEvents(){
  var back = document.getElementById('back-to-ops');
  if (back) back.addEventListener('click', function(){ goPage('operaciones'); });
}

function renderEvents(opId){
  var evs = opId === TARGET_OP_ID ? eventData : [];
  var tbody = document.getElementById('events-tbody');
  tbody.innerHTML = evs.map(function(ev, i){
    return '<tr><td colspan="5" style="padding:0;"><div class="event-row-main" data-idx="' + i + '">' +
      '<div class="event-col" style="width:24px;color:#999;" id="ev-icon-' + i + '"><i class="ti ti-chevron-right"></i></div>' +
      '<div class="event-col" style="width:120px;color:#555;">' + ev.date + '</div>' +
      '<div class="event-col" style="width:100px;"><span class="type-info">' + ev.type + '</span></div>' +
      '<div class="event-col" style="width:140px;color:#555;">' + ev.origen + '</div>' +
      '<div class="event-col" style="color:#555;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:180px;">' + ev.msg + '</div>' +
    '</div><div class="event-output" id="ev-out-' + i + '"><div class="output-text">' + ev.output + '</div></div></td></tr>';
  }).join('');
  tbody.querySelectorAll('.event-row-main').forEach(function(row){
    row.addEventListener('click', function(){ toggleEvent(parseInt(row.dataset.idx,10)); });
  });
  wireOpDetailEvents();
}

function toggleEvent(i){
  var out = document.getElementById('ev-out-' + i);
  var icon = document.getElementById('ev-icon-' + i);
  var isOpen = out.classList.contains('open');
  out.classList.toggle('open');
  icon.innerHTML = isOpen ? '<i class="ti ti-chevron-right"></i>' : '<i class="ti ti-chevron-down"></i>';
}

function pageFlujos(){
  var rows = [
    ["Compatibilidad Windows 11","Compatibilidad Windows ...","Workspace","23h 0m 0s","Deshabilitado"],
    ["Tarea programada","Tarea programada","Workspace","24h 0m 0s","Deshabilitado"],
    ["Reiniciar Servicio Imp","Reiniciar Servicio","Sesión","1h 0m 0s","Deshabilitado"]
  ];
  var rowsHtml = rows.map(function(r){ return '<tr><td class="desc-link">' + r[0] + '</td><td>' + r[1] + '</td><td>' + r[2] + '</td><td>' + r[3] + '</td><td>' + r[4] + '</td></tr>'; }).join('');
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Flexxible Training Site - Flujos</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-plus"></i> Nuevo</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div class="btn-tool"><i class="ti ti-refresh"></i> Recargar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Descripción</th><th>Tipo</th><th>Tiempo de re...</th><th>Habilitado</th></tr></thead><tbody>' + rowsHtml + '</tbody></table></div>' +
  '<div class="pager"><span></span><span>Página 1 de 1 · 1 a 3 de 3 resultados</span><span style="font-size:11px;color:#aaa;">Tamaño de página: 50</span></div></div>';
}

function pageInformes(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Flexxible Training Site - Informes</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div class="btn-tool"><i class="ti ti-refresh"></i> Recargar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div><div class="filter-chip">Filtrar</div></div>' +
  '<div class="page" style="padding:0 20px;"><div class="report-grid">' +
    '<div class="report-card"><div class="report-card-title">Inventario Dispositivos: RAM y Espacio en Disco</div><div class="report-card-sub">Personales</div><div class="report-shared"><i class="ti ti-share"></i> Compartido</div><button class="report-btn">Ver detalles</button></div>' +
    '<div class="report-card"><div class="report-card-title">Workspaces by Processor Model</div><div class="report-card-sub">Workspaces</div><div class="report-shared"><i class="ti ti-share"></i> Compartido</div><button class="report-btn">Ver detalles</button></div>' +
  '</div></div></div>';
}

function pageCrearIA(){
  var cats = [
    ["Workspaces","layout-grid",["¿Cuántos Workspaces tienen actualizaciones pendientes?","Muéstrame Workspaces por sistema operativo"]],
    ["Seguridad y Cumplimiento","shield",["¿Qué Workspaces tienen problemas de antivirus?","Lista de Workspaces que no están encriptados"]],
    ["Hardware y rendimiento","cpu",["¿Qué workspaces tienen más RAM instalada?","Listar workspaces por modelo de procesador"]],
    ["VDI y virtualización","cloud",["¿Cuántos workspaces son Azure Virtual Desktop?","Muéstrame workspaces por hipervisor"]]
  ];
  var catsHtml = cats.map(function(c){
    var qs = c[2].map(function(q){ return '<div class="ia-q">' + q + '</div>'; }).join('');
    return '<div class="ia-cat"><div class="ia-cat-title"><i class="ti ti-' + c[1] + '"></i> ' + c[0] + '</div>' + qs + '</div>';
  }).join('');
  return '<div class="page"><div class="page-header">' + enunciadoHtml() +
    '<div style="font-size:18px;font-weight:600;color:#1a1a1a;text-align:center;margin-bottom:12px;">Crear con IA: Informes</div>' +
    '<div class="ia-hint"><i class="ti ti-info-circle"></i> Si necesitas ayuda, consulta la documentación. Cualquier IA puede cometer errores.</div>' +
    '<div class="ia-box"><div class="ia-input">Haz una pregunta sobre tus datos...</div></div>' +
    '<div style="text-align:center;color:#888;font-size:12px;margin-bottom:10px;">O prueba estas consultas</div>' +
    '<div class="ia-grid">' + catsHtml + '</div></div></div>';
}

function pageInquilinos(){
  var rows = ["Bimbo","Bimbo","Flexxible Training Site (tu inquilino)","IT LAB","Ingeniería LAB","Sanitari","Universidad de Barcelona"];
  var rowsHtml = rows.map(function(r){ return '<tr><td class="desc-link">' + r + '</td><td>FlexxClient</td><td>—</td><td class="desc-link">Ver detalle</td></tr>'; }).join('');
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Flexxible Training Site - Inquilinos</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-plus"></i> Nuevo</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Producto</th><th>Fecha de creación</th><th>Acción</th></tr></thead><tbody>' + rowsHtml + '</tbody></table></div></div>';
}

function pageActivacion(){
  var rows = [["Ingeniería LAB","Active"],["IT LAB","Active"],["Sanitari","Active"],["Bimbo","Active"]];
  var rowsHtml = rows.map(function(r){ return '<tr><td class="desc-link">Flexxible Training Site &gt; ' + r[0] + '</td><td>FlexxClient</td><td style="color:#16a34a;">● ' + r[1] + '</td></tr>'; }).join('');
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Activaciones — Flexxible Training Site</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Producto</th><th>Estado</th></tr></thead><tbody>' + rowsHtml + '</tbody></table></div></div>';
}

var alertRows = [
  {ws:"",info:"Drive: C: Free space: 2 GB, low storage warning triggered on system drive",fecha:"20/8/25, 11:44:09",elem:"Device: DESKTOP-3GAB2JS",grav:"Critical",sc:"crit"},
  {ws:"5CD54685XF",info:"Drive: C: Free space: 74 GB, storage usage approaching threshold",fecha:"13/8/26, 23:00:39",elem:"Device: 5CD54685XF",grav:"Critical",sc:"crit"},
  {ws:"5CD54685XF",info:"Drive: C: Free space: 74 GB, storage usage approaching threshold",fecha:"13/8/26, 20:12:49",elem:"Device: 5CD54685XF",grav:"Warning",sc:"warn"},
  {ws:"AEC-5HDHJR3",info:"Workspace with 2 Plug and Play devices requiring driver updates",fecha:"13/8/26, 20:41:35",elem:"Device: AEC-5HDHJR3",grav:"Warning",sc:"warn"}
];

function pageAlertas(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Flexxible Training Site - Alertas activas</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input type="text" id="alerts-search" placeholder="Buscar por término..."></div><div class="filter-chip">Categoría: <b>Cualquiera</b></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Workspace</th><th>Información</th><th>Fecha de inicio</th><th>Elemento</th><th>Gravedad</th></tr></thead><tbody id="alerts-tbody"></tbody></table></div>' +
  '<div style="padding:8px 18px;font-size:11px;color:#888;" id="alerts-count"></div></div>';
}

function renderAlertas(filterText){
  var tbody = document.getElementById('alerts-tbody');
  if (!tbody) return;
  var q = (filterText || '').trim().toLowerCase();
  var filtered = q === '' ? alertRows : alertRows.filter(function(r){
    return r.ws.toLowerCase().indexOf(q) !== -1 ||
           r.info.toLowerCase().indexOf(q) !== -1 ||
           r.elem.toLowerCase().indexOf(q) !== -1 ||
           r.grav.toLowerCase().indexOf(q) !== -1;
  });
  tbody.innerHTML = filtered.map(function(r){
    return '<tr><td>' + r.ws + '</td><td>' + r.info + '</td><td>' + r.fecha + '</td><td>' + r.elem + '</td><td class="status-' + (r.sc==='crit'?'crit':'warn') + '">' + r.grav + '</td></tr>';
  }).join('');
  var countEl = document.getElementById('alerts-count');
  if (countEl) countEl.textContent = filtered.length + ' resultado' + (filtered.length === 1 ? '' : 's');
}

function pageAlertConfig(){
  var rows = [
    ["Boot duration","Critical","Rendimiento","90","seconds"],
    ["Critical event log","Critical","Registros de eventos","1",""],
    ["Event alert","Informational","Registros de eventos","720","minutes"],
    ["High CPU usage for Workspace","Critical","Rendimiento","30","%"],
    ["High RAM usage for Workspace","Warning","Rendimiento","90","%"]
  ];
  var rowsHtml = rows.map(function(r){ return '<tr><td class="desc-link">' + r[0] + '</td><td class="status-' + (r[1]==='Critical'?'crit':r[1]==='Warning'?'warn':'ok') + '">' + r[1] + '</td><td>' + r[2] + '</td><td>' + r[3] + '</td><td>' + r[4] + '</td></tr>'; }).join('');
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Flexxible Training Site - Configuración de alertas</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-plus"></i> Nuevo</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Gravedad</th><th>Categoría</th><th>Umbral</th><th>Unidad</th></tr></thead><tbody>' + rowsHtml + '</tbody></table></div></div>';
}

/* ===================== WORKSPACES ===================== */
var wsRows = [
  {nombre:"11LAP1JY0V74.indra.es",estado:"Desconectado",ip:"10.22.192.9",grupo:"Oficina Indra",tipo:"Físico",conex:"Ethernet",ultimo:"21/8/26, 14:59:01"},
  {nombre:"5CD54685XF",estado:"Desconectado",ip:"192.168.1.151",grupo:"RP Training",tipo:"Físico",conex:"Wifi",ultimo:"13/8/26, 23:44:58"},
  {nombre:"AEC-5HDHJR3",estado:"Desconectado",ip:"172.20.156.93",grupo:"RP Training",tipo:"Físico",conex:"Wifi",ultimo:"14/8/26, 0:27:00"},
  {nombre:"DESKTOP-DEFE7N5",estado:"Desconectado",ip:"192.168.1.131",grupo:"RP Training",tipo:"Virtual",conex:"Ethernet",ultimo:"1/9/26, 11:49:01"},
  {nombre:"LAPTOP-B1TODCH9",estado:"Desconectado",ip:"-",grupo:"RP Training",tipo:"Físico",conex:"-",ultimo:"20/8/26, 8:30:07"}
];

function pageWorkspaces(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Flexxible Training Site - Workspaces</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-device-desktop"></i> Asistencia remota</div><div class="btn-tool"><i class="ti ti-trash"></i> Eliminar workspaces</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input type="text" id="ws-search" placeholder="Buscar por término..."></div><div class="filter-chip">Aplicaciones: <b>Cualquiera</b></div><div class="filter-chip">Grupos de workspaces: <b>Cualquiera</b></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Estado</th><th>Dirección IP</th><th>Grupo de reporte</th><th>Tipo de dispositivo</th><th>Conexión</th><th>Último informe</th></tr></thead><tbody id="ws-tbody"></tbody></table></div>' +
  '<div style="padding:8px 18px;font-size:11px;color:#888;" id="ws-count"></div></div>';
}

function renderWorkspaces(filterText){
  var tbody = document.getElementById('ws-tbody');
  if (!tbody) return;
  var q = (filterText || '').trim().toLowerCase();
  var filtered = q === '' ? wsRows : wsRows.filter(function(r){
    return r.nombre.toLowerCase().indexOf(q) !== -1 ||
           r.ip.toLowerCase().indexOf(q) !== -1 ||
           r.grupo.toLowerCase().indexOf(q) !== -1 ||
           r.tipo.toLowerCase().indexOf(q) !== -1;
  });
  tbody.innerHTML = filtered.map(function(r){
    return '<tr><td class="desc-link">' + r.nombre + '</td><td>' + r.estado + '</td><td>' + r.ip + '</td><td>' + r.grupo + '</td><td>' + r.tipo + '</td><td>' + r.conex + '</td><td>' + r.ultimo + '</td></tr>';
  }).join('');
  var countEl = document.getElementById('ws-count');
  if (countEl) countEl.textContent = filtered.length + ' resultado' + (filtered.length === 1 ? '' : 's');
}

function pageSesiones(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Sesiones</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Usuario</th><th>Workspace</th><th>Inicio de sesión</th><th>Estado</th></tr></thead><tbody>' +
  '<tr><td class="desc-link">jserra@flexxible.com</td><td>DESKTOP-DEFE7N5</td><td>1/9/26, 08:12:03</td><td class="status-ok">Activa</td></tr>' +
  '<tr><td class="desc-link">Training</td><td>5CD54685XF</td><td>31/8/26, 17:40:22</td><td class="status-warn">Inactiva</td></tr>' +
  '</tbody></table></div></div>';
}

function pageGruposWorkspaces(){
  var rows = [
    ["Dispositivos Encendidos","Dinámico","0"],
    ["Dispositivos W11","Estático","1"],
    ["Equipos sin actualizar más de 30 días","Dinámico","2"],
    ["Filtro Test Dinamico","Estático","0"],
    ["Grupo Simón","Estático","0"],
    ["Grupo dinamico Prueba","Dinámico","0"],
    ["Grupo estático","Estático","1"],
    ["Grupo sin seguridad","Estático","4"],
    ["Menos de 80%","Dinámico","5"],
    ["Máquinas encendidas","Dinámico","0"],
    ["Otra prueba de lio","Estático","0"]
  ];
  var rowsHtml = rows.map(function(r){
    var clickable = r[0] === 'Grupo sin seguridad';
    return '<tr' + (clickable ? ' class="clickable" data-gws="1"' : '') + '><td class="desc-link">' + r[0] + '</td><td>' + r[1] + '</td><td>' + r[2] + '</td></tr>';
  }).join('');
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Flexxible Training Site - Grupos de Workspaces</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-plus"></i> Nuevo</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Tipo</th><th># Workspaces</th></tr></thead><tbody>' + rowsHtml + '</tbody></table></div></div>';
}

function pageUbicaciones(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Ubicaciones</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-plus"></i> Nuevo</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Dirección</th></tr></thead><tbody>' +
  '<tr><td class="desc-link">Terrassa</td><td>Carrer de Vallhonrat, 45</td></tr>' +
  '</tbody></table></div></div>';
}

function pageRedes(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Redes</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Red</th><th>Tipo</th><th>Workspaces conectados</th></tr></thead><tbody>' +
  '<tr><td class="desc-link">RP Training - LAN</td><td>Ethernet</td><td>3</td></tr>' +
  '<tr><td class="desc-link">Oficina Indra - LAN</td><td>Ethernet</td><td>1</td></tr>' +
  '</tbody></table></div></div>';
}

function pageNotificaciones(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Notificaciones</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-plus"></i> Nuevo</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Destinatarios</th><th>Estado</th></tr></thead><tbody>' +
  '<tr><td class="desc-link">Baja de batería crítica</td><td>Equipos</td><td class="status-ok">Habilitado</td></tr>' +
  '</tbody></table></div></div>';
}

var wifiRows = [
  {ssid:"CHAKONEN",isp:"XFERA Moviles S.A",pob:"Villovieco",pais:"ES",ws:"DESKTOP-HB4T4RK"},
  {ssid:"AP_4LT4M1R4N0",isp:"America Movil Peru S.A.C",pob:"Lima",pais:"PE",ws:"LALTAMIRANO10.indra.es"},
  {ssid:"AYESA",isp:"",pob:"Madrid",pais:"ES",ws:"—"},
  {ssid:"Ayesa_PDA",isp:"",pob:"Madrid",pais:"ES",ws:"DESKTOP-F32NGIC"},
  {ssid:"CASAREAL",isp:"Telefonica De Espana S.A.U.",pob:"Madrid",pais:"ES",ws:"PRUEBAS-EREAL"},
  {ssid:"Chakonen",isp:"Xtra Telecom S.A.",pob:"Carcastillo",pais:"ES",ws:"DESKTOP-HB4T4RK"},
  {ssid:"CSC-Administracion_5G",isp:"Xtra Telecom S.A.",pob:"La Pobla de Farnals",pais:"ES",ws:"DESKTOP-HB4T4RK"},
  {ssid:"D76E",isp:"",pob:"Madrid",pais:"ES",ws:"11LAP1JY0V74.indra.es"},
  {ssid:"Deusto Seidor - Invitados",isp:"SAREnet, S.A",pob:"Madrid",pais:"ES",ws:"—"},
  {ssid:"DIGIFIBRA-C6B7",isp:"Digi Spain Telecom S.L.U.",pob:"Usera",pais:"ES",ws:"11LAP5CG9324KWY.indra..."},
  {ssid:"DIGIFIBRA-PLUS-2kAR",isp:"",pob:"Seville",pais:"ES",ws:"DESKTOP-IFE1SD5"},
  {ssid:"DIGIFIBRA-PLUS-dCcH",isp:"Digi Spain Telecom S.L.U.",pob:"Vitoria-Gasteiz",pais:"ES",ws:"Ei003811"}
];

function pageRedesInalambricas(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Redes inalámbricas</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input type="text" id="wifi-search" placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>SSID</th><th>ISP</th><th>Población</th><th>País</th><th>Workspace detectado</th></tr></thead><tbody id="wifi-tbody"></tbody></table></div>' +
  '<div style="padding:8px 18px;font-size:11px;color:#888;" id="wifi-count"></div></div>';
}

function renderRedesInalambricas(filterText){
  var tbody = document.getElementById('wifi-tbody');
  if (!tbody) return;
  var q = (filterText || '').trim().toLowerCase();
  var filtered = q === '' ? wifiRows : wifiRows.filter(function(r){
    return r.ssid.toLowerCase().indexOf(q) !== -1 ||
           r.isp.toLowerCase().indexOf(q) !== -1 ||
           r.pob.toLowerCase().indexOf(q) !== -1 ||
           r.ws.toLowerCase().indexOf(q) !== -1;
  });
  tbody.innerHTML = filtered.map(function(r){
    return '<tr><td class="desc-link">' + r.ssid + '</td><td>' + r.isp + '</td><td>' + r.pob + '</td><td>' + r.pais + '</td><td>' + r.ws + '</td></tr>';
  }).join('');
  var countEl = document.getElementById('wifi-count');
  if (countEl) countEl.textContent = filtered.length + ' resultado' + (filtered.length === 1 ? '' : 's');
}

/* ===================== ACTUALIZACIONES ===================== */
function pageActResumen(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Resumen</div></div>' +
  '<div style="padding:0 20px;display:grid;grid-template-columns:1fr 1fr;gap:24px;">' +
    '<div><div style="font-weight:600;margin-bottom:10px;">Targets</div>' +
      '<div class="report-card" style="text-align:left;margin-bottom:10px;"><b style="color:#c87d30;">⚠ Alertas (1)</b><div style="font-size:13px;margin-top:6px;">Grupos de reporte sin una directiva de actualizaciones asignada</div></div>' +
      '<div class="report-card" style="text-align:left;margin-bottom:10px;"><b style="color:#2563eb;">ℹ Información (1)</b><div style="font-size:13px;margin-top:6px;">¡Excelente trabajo! Todos los objetivos tienen horarios asignados</div></div>' +
      '<div style="display:flex;gap:16px;"><div class="report-card"><div style="font-size:28px;font-weight:700;">38%</div><div style="font-size:11px;color:#888;">3 grupos de reporte</div><div style="font-size:12px;">Grupos de reporte sin una directiva de actualización</div></div>' +
      '<div class="report-card"><div style="font-size:28px;font-weight:700;">0%</div><div style="font-size:11px;color:#888;">0 objetivos</div><div style="font-size:12px;">Objetivos sin una programación</div></div></div>' +
    '</div>' +
    '<div><div style="font-weight:600;margin-bottom:10px;">Workspaces</div>' +
      '<div class="report-card" style="text-align:left;margin-bottom:10px;"><b style="color:#2563eb;">ℹ Información (1)</b><div style="font-size:13px;margin-top:6px;">¡Excelente trabajo! Todos los Workspaces tienen asignado un grupo de reporte</div></div>' +
      '<div class="report-card"><div style="font-size:28px;font-weight:700;">0</div><div style="font-size:11px;color:#888;">5 workspaces en total</div><div style="font-size:12px;">Workspaces sin Grupo de Reporte</div></div>' +
    '</div>' +
  '</div></div>';
}

function pieChartHtml(data, size){
  var total = 0;
  data.forEach(function(d){ total += d.value; });
  var cx = size/2, cy = size/2, r = size/2 - 6;
  var angle = -90;
  var paths = '';
  data.forEach(function(d){
    if (total <= 0 || d.value <= 0) return;
    var slice = (d.value/total)*360;
    var a1 = angle * Math.PI/180;
    var x1 = cx + r*Math.cos(a1), y1 = cy + r*Math.sin(a1);
    var endAngle = angle + slice;
    var a2 = endAngle * Math.PI/180;
    var x2 = cx + r*Math.cos(a2), y2 = cy + r*Math.sin(a2);
    var largeArc = slice > 180 ? 1 : 0;
    paths += '<path d="M' + cx + ',' + cy + ' L' + x1.toFixed(2) + ',' + y1.toFixed(2) +
      ' A' + r + ',' + r + ' 0 ' + largeArc + ' 1 ' + x2.toFixed(2) + ',' + y2.toFixed(2) +
      ' Z" fill="' + d.color + '"></path>';
    angle = endAngle;
  });
  var legend = data.map(function(d){
    return '<div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#333;margin-bottom:8px;">' +
      '<span style="width:11px;height:11px;border-radius:50%;background:' + d.color + ';display:inline-block;flex-shrink:0;"></span>' +
      '<b>' + d.label + '</b></div>';
  }).join('');
  return '<div style="display:flex;align-items:center;gap:36px;flex-wrap:wrap;">' +
    '<svg width="' + size + '" height="' + size + '" viewBox="0 0 ' + size + ' ' + size + '">' + paths + '</svg>' +
    '<div>' + legend + '</div></div>';
}

var grupoReporteData = [
  {label:"RP Training", value:4, color:"#8ab4f8"},
  {label:"RP Training 2", value:0, color:"#3a3a3a"},
  {label:"Aeronáutica", value:0, color:"#8ce99a"},
  {label:"XRTraining", value:0, color:"#f5a623"},
  {label:"UPCT – Departamento TIC", value:0, color:"#6c5ce7"},
  {label:"Prueba Rol específico", value:0, color:"#e64980"},
  {label:"Oficina Indra", value:1, color:"#e6d94d"},
  {label:"Prueba Laboratorio VM", value:0, color:"#2f9e7a"}
];

function pageActGrupos(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Gestión de actualizaciones: grupos de reporte</div></div>' +
  '<div style="padding:0 20px;display:flex;gap:16px;margin-bottom:16px;">' +
    '<div class="report-card"><div style="font-size:24px;font-weight:700;">5</div><div style="font-size:11px;color:#888;">Total workspaces</div></div>' +
    '<div class="report-card"><div style="font-size:24px;font-weight:700;">5</div><div style="font-size:11px;color:#888;">Windows workspaces</div></div>' +
    '<div class="report-card"><div style="font-size:24px;font-weight:700;">0</div><div style="font-size:11px;color:#888;">Linux workspaces</div></div>' +
  '</div>' +
  '<div style="padding:0 20px;">' +
    '<div style="font-size:15px;font-weight:600;color:#333;margin-bottom:14px;">Total workspaces por grupo de reporte</div>' +
    pieChartHtml(grupoReporteData, 200) +
  '</div></div>';
}

var patchRows = [
  ["2267602","Security Intelligence Update for Microsoft Defender Antivirus - KB2267602 (Version 1.457.441.0)","Definition Update","Microsoft Defender Antivirus","2/9/26"],
  ["-","Microsoft Edge-Extended Stable Channel Version 152 Update for x86 based Editions","Updates","Microsoft Edge","2/9/26"],
  ["-","Intel Corporation ComputeAccelerator Driver Update (32.0.100.4841)","Drivers","Windows 11 Client","2/9/26"],
  ["-","Dell, Inc. Firmware Driver Update (0.1.35.0)","Drivers","Windows 11 Client","2/9/26"],
  ["-","Microsoft Edge-WebView2 Runtime Version 152 Update for x64 based Editions","Updates","Microsoft Edge","2/9/26"]
];
function pageActPatches(){
  var rowsHtml = patchRows.map(function(r){ return '<tr><td>' + r[0] + '</td><td class="desc-link">' + r[1] + '</td><td>' + r[2] + '</td><td>' + r[3] + '</td><td>' + r[4] + '</td></tr>'; }).join('');
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Parches de Microsoft</div></div>' +
  '<div class="toolbar"><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>KB</th><th>Descripción de revisión</th><th>Clasificación</th><th>Producto</th><th>Fecha de lanzamiento</th></tr></thead><tbody>' + rowsHtml + '</tbody></table></div></div>';
}

function pageActDirectivas(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Directivas de actualizaciones de Microsoft</div></div>' +
  '<div class="toolbar"><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar directiva de actualizaciones de Windows..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Objetivos de la directiva</th><th>Aprobaciones automáticas</th></tr></thead><tbody>' +
  '<tr><td class="desc-link">Directiva de parches</td><td class="desc-link">Prueba para directiva de actualización</td><td class="status-ok">● Habilitado</td></tr>' +
  '</tbody></table></div></div>';
}

function pageActDestinatarios(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">Destinatarios</div></div>' +
  '<div class="toolbar"><div class="btn-tool"><i class="ti ti-plus"></i> Nuevo</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div style="flex:1"></div><div class="search-box"><i class="ti ti-search"></i><input placeholder="Buscar por término..."></div></div>' +
  '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Grupos de reporte</th><th>Tiene programación establecida</th></tr></thead><tbody>' +
  '<tr><td class="desc-link">Prueba para directiva de actualización</td><td>RP Training 2</td><td>✓</td></tr>' +
  '<tr><td class="desc-link">Equipos</td><td>RT, OI, PV</td><td>✓</td></tr>' +
  '</tbody></table></div></div>';
}

/* ===================== DETALLE GRUPO DE WORKSPACES (ejercicio de programación) ===================== */

var gwsWorkspaces = [
  {nombre:"11LAP1JY0V74.indra.es",fqdn:"11LAP1JY0V74.indra.es",ip:"10.22.192.9",so:"Microsoft Windows 11 Pro 25H2",cpu:"14",ram:"15828",tipo:"Physical device"},
  {nombre:"5CD54685XF",fqdn:"5CD54685XF",ip:"192.168.1.151",so:"Microsoft Windows 11 Pro 25H2",cpu:"12",ram:"15645",tipo:"Physical device"},
  {nombre:"DESKTOP-DEFE7N5",fqdn:"DESKTOP-DEFE7N5",ip:"192.168.1.131",so:"Microsoft Windows 10 Enterprise Evaluation",cpu:"4",ram:"2489",tipo:"Virtual Desktop"},
  {nombre:"AEC-5HDHJR3",fqdn:"AEC-5HDHJR3",ip:"172.20.156.93",so:"Microsoft Windows 11 Pro 24H2",cpu:"8",ram:"15761",tipo:"Physical device"}
];

var gwsApps = [
  ["7-Zip 23.01 (x64)","Igor Pavlov","23.01","Windows","1"],
  ["7-Zip 26.02 (x64 edition)","Igor Pavlov","26.02.00.0","Windows","1"],
  ["Adobe Acrobat (64-bit)","Adobe","26.001.21662","Windows","1"],
  ["Aplicaciones de Microsoft 365 para empresas","Microsoft Corporation","16.0.20026.20168","Windows","1"],
  ["Aplicaciones de Microsoft 365 para empresas","Microsoft Corporation","16.0.20228.20186","Windows","1"],
  ["Blender","Blender Foundation","5.1.1","Windows","1"],
  ["Calculator","Microsoft Corporation","11.2508.0","Windows","1"],
  ["Calculator","Microsoft Corporation","11.2606.0","Windows","1"],
  ["Calendar","Microsoft Corporation","2.2602.0","Windows","1"]
];

var gwsHistorial = ["ago 21st","ago 22nd","ago 23rd","ago 24th","ago 25th","ago 26th","ago 27th","ago 28th","ago 29th","ago 30th","ago 31st","sept 1st","sept 2nd","sept 3rd","sept 4th","sept 5th"];

function barChartHtml(labels, values, maxVal){
  var bars = values.map(function(v){
    var h = maxVal > 0 ? (v/maxVal)*100 : 0;
    return '<div class="bar-chart-bar" style="height:' + h + '%;" title="' + v + '"></div>';
  }).join('');
  var lbls = labels.map(function(l){ return '<span>' + l + '</span>'; }).join('');
  return '<div class="bar-chart-wrap">' + bars + '</div><div class="bar-chart-labels">' + lbls + '</div>';
}

function pageGrupoWSDetail(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() +
    '<div class="breadcrumb"><a id="gws-back-1">Flexxible Training Site</a><i class="ti ti-chevron-right" style="font-size:11px;"></i><a id="gws-back-2">Grupos de Workspaces</a><i class="ti ti-chevron-right" style="font-size:11px;"></i><span style="color:#555;">Grupo sin seguridad</span></div>' +
    '<div style="font-size:20px;font-weight:700;color:#1a1a1a;">Grupo sin seguridad</div>' +
    '<div class="gws-tabs">' +
      '<div class="gws-tab" data-tab="detalles">Detalles del grupo de Workspaces</div>' +
      '<div class="gws-tab" data-tab="workspaces">Workspaces</div>' +
      '<div class="gws-tab" data-tab="historial">Historial</div>' +
      '<div class="gws-tab" data-tab="ubicacion">Ubicación</div>' +
      '<div class="gws-tab" data-tab="aplicaciones">Aplicaciones instaladas</div>' +
      '<div class="gws-tab" data-tab="programaciones">Programaciones</div>' +
    '</div>' +
  '</div>' +
  '<div class="page" style="padding:0 20px;"><div class="gws-panel" id="gws-tab-content"></div></div></div>';
}

function wireGrupoWSTabs(){
  document.getElementById('gws-back-1').addEventListener('click', function(){ goPage('inicio'); });
  document.getElementById('gws-back-2').addEventListener('click', function(){ goPage('gruposworkspaces'); });
  document.querySelectorAll('.gws-tab').forEach(function(t){
    t.addEventListener('click', function(){ renderGrupoWSTab(t.dataset.tab); });
  });
}

function renderGrupoWSTab(tab){
  grupoWSState.activeTab = tab;
  document.querySelectorAll('.gws-tab').forEach(function(t){ t.classList.toggle('active', t.dataset.tab === tab); });
  var el = document.getElementById('gws-tab-content');
  if (!el) return;

  if (tab === 'detalles'){
    el.innerHTML = '<div style="display:grid;grid-template-columns:2fr 1fr;gap:20px;">' +
      '<div class="gws-card">' +
        '<div class="gws-field-label">Nombre</div><div class="gws-field-value">Grupo sin seguridad</div>' +
        '<div class="gws-field-label">Descripción</div><div class="gws-field-value">-</div>' +
        '<div class="gws-field-label">Tipo</div><div class="gws-field-value">Estático</div>' +
      '</div>' +
      '<div>' +
        '<div class="gws-side-box"><i class="ti ti-stack"></i><div><div class="gws-side-label"># Workspaces</div><div class="gws-side-value">4</div></div></div>' +
        '<div class="gws-side-box"><i class="ti ti-users"></i><div><div class="gws-side-label">Creado por</div><div class="gws-side-value">Joan Serra</div></div></div>' +
        '<div class="gws-side-box"><i class="ti ti-calendar"></i><div><div class="gws-side-label">Fecha de creación</div><div class="gws-side-value">21/8/26</div></div></div>' +
      '</div></div>';
  }
  else if (tab === 'workspaces'){
    var rows = gwsWorkspaces.map(function(w){
      return '<tr><td class="desc-link">' + w.nombre + '</td><td>' + w.fqdn + '</td><td>' + w.ip + '</td><td>' + w.so + '</td><td>' + w.cpu + '</td><td>' + w.ram + '</td><td>' + w.tipo + '</td></tr>';
    }).join('');
    el.innerHTML = '<div class="toolbar" style="padding:0 0 10px;background:transparent;border:none;"><div class="btn-tool"><i class="ti ti-upload"></i> Importar Workspaces</div><div class="btn-tool"><i class="ti ti-pencil"></i> Editar</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div></div>' +
      '<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>FQDN</th><th>Dirección IP</th><th>Sistema operativo</th><th>Núcleos de CPU</th><th>RAM</th><th>Tipo</th></tr></thead><tbody>' + rows + '</tbody></table></div>';
  }
  else if (tab === 'historial'){
    var vals = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0];
    el.innerHTML = '<div style="font-size:14px;color:#888;margin-bottom:10px;">Workspaces por día</div>' + barChartHtml(gwsHistorial, vals, 5);
  }
  else if (tab === 'ubicacion'){
    el.innerHTML = '<div style="display:grid;grid-template-columns:1fr 1.3fr;gap:20px;">' +
      '<div>' +
        '<div class="gws-field-label">Dirección</div><div class="gws-field-value">Carrer de Vallhonrat, 08221 Terrassa, Barcelona, España</div>' +
        '<div class="gws-field-label">Descripción</div><div class="gws-field-value">-</div>' +
        '<button class="sp-btn sp-btn-cancel">Editar</button>' +
      '</div>' +
      '<div style="background:#e8ecef;border-radius:8px;height:260px;display:flex;align-items:center;justify-content:center;color:#888;font-size:12px;"><i class="ti ti-map-pin" style="font-size:24px;margin-right:6px;color:#c0392b;"></i> Carrer de Vallhonrat (mapa)</div>' +
    '</div>';
  }
  else if (tab === 'aplicaciones'){
    var appRows = gwsApps.map(function(a){
      return '<tr><td class="desc-link">' + a[0] + '</td><td>' + a[1] + '</td><td>' + a[2] + '</td><td>' + a[3] + '</td><td>' + a[4] + '</td></tr>';
    }).join('');
    el.innerHTML = '<div style="background:#f5f4f0;border:0.5px solid #e0dfd8;border-radius:6px;padding:8px 12px;font-size:12px;color:#666;margin-bottom:12px;"><i class="ti ti-info-circle"></i> Los datos se actualizan cada 2 horas. Es posible que los cambios recientes aún no se reflejen.</div>' +
      '<div class="table-wrap"><table><thead><tr><th>Aplicación</th><th>Editor</th><th>Versión</th><th>Sistema operativo</th><th># Workspaces</th></tr></thead><tbody>' + appRows + '</tbody></table></div>' +
      '<div style="padding:8px 0;font-size:11px;color:#888;">Mostrando 1 a 50 de 131 resultados</div>';
  }
  else if (tab === 'programaciones'){
    renderProgramacionesTab(el);
  }
}

function renderProgramacionesTab(el){
  var toolbar = '<div class="toolbar" style="padding:0 0 10px;background:transparent;border:none;"><div class="btn-tool" id="gws-nuevo-prog"><i class="ti ti-plus"></i> Nuevo</div><div class="btn-tool"><i class="ti ti-file-export"></i> Exportar</div><div class="btn-tool"><i class="ti ti-refresh"></i> Recargar</div></div>';
  var body;
  if (grupoWSState.programaciones.length === 0){
    body = '<div class="gws-empty"><i class="ti ti-package"></i>No hay programaciones configuradas</div>';
  } else {
    var rows = grupoWSState.programaciones.map(function(p){
      return '<tr><td class="desc-link">' + p.accionLabel + '</td><td>' + p.resumen + '</td><td>' + p.zonaLabel + '</td></tr>';
    }).join('');
    body = '<div class="table-wrap"><table><thead><tr><th>Acción</th><th>Programación</th><th>Zona horaria</th></tr></thead><tbody>' + rows + '</tbody></table></div>';
  }
  el.innerHTML = toolbar + body;
  var btn = document.getElementById('gws-nuevo-prog');
  if (btn) btn.addEventListener('click', openSidePanel);
}

/* ---- Panel lateral "Nueva acción programada" ---- */
function openSidePanel(){
  document.getElementById('sp-accion').value = '';
  document.getElementById('sp-hora').value = '';
  document.getElementById('sp-zona').value = '';
  document.querySelectorAll('.sp-day-item input').forEach(function(cb){ cb.checked = false; });
  document.getElementById('sp-hora-err').style.display = 'none';
  document.getElementById('sp-dias-err').style.display = 'none';
  document.getElementById('sp-zona-err').style.display = 'none';
  document.getElementById('sp-hora').classList.remove('err');
  document.getElementById('sp-overlay').classList.add('open');
}
function closeSidePanel(){
  document.getElementById('sp-overlay').classList.remove('open');
}

function submitProgramacion(){
  var accionSel = document.getElementById('sp-accion');
  var hora = document.getElementById('sp-hora').value;
  var zonaSel = document.getElementById('sp-zona');
  var diasChecked = Array.prototype.slice.call(document.querySelectorAll('.sp-day-item input:checked')).map(function(cb){ return cb.value; });

  var horaErr = document.getElementById('sp-hora-err');
  var diasErr = document.getElementById('sp-dias-err');
  var zonaErr = document.getElementById('sp-zona-err');
  var horaInput = document.getElementById('sp-hora');

  var valid = true;
  if (!hora){ horaErr.style.display = 'block'; horaInput.classList.add('err'); valid = false; }
  else { horaErr.style.display = 'none'; horaInput.classList.remove('err'); }

  if (diasChecked.length === 0){ diasErr.style.display = 'block'; valid = false; }
  else { diasErr.style.display = 'none'; }

  if (!zonaSel.value){ zonaErr.style.display = 'block'; valid = false; }
  else { zonaErr.style.display = 'none'; }

  if (!accionSel.value) valid = false;

  if (!valid) return;

  var accionLabel = accionSel.options[accionSel.selectedIndex].text;
  var zonaLabel = zonaSel.options[zonaSel.selectedIndex].text;
  var diasTexto = diasChecked.length === 1 ? ('sólo el ' + diasChecked[0].toLowerCase())
    : ('sólo ' + diasChecked.slice(0,-1).map(function(d){return d.toLowerCase();}).join(', ') + ' y ' + diasChecked[diasChecked.length-1].toLowerCase());
  var resumen = 'A las ' + hora + ', ' + diasTexto;

  grupoWSState.programaciones.push({ accionLabel: accionLabel, resumen: resumen, zonaLabel: zonaLabel, accionValue: accionSel.value });

  closeSidePanel();
  renderGrupoWSTab('programaciones');

  if (accionSel.value === 'apagar'){
    document.getElementById('token-title').textContent = '¡Programación de apagado creada correctamente!';
    document.getElementById('token-sub').textContent = 'Copia este código y pégalo en la pregunta correspondiente de Evolcampus:';
    document.getElementById('token-box').textContent = TOKEN_PROGRAMACION_APAGADO;
    document.getElementById('token-box').style.display = 'block';
    document.getElementById('copy-token-btn').style.display = 'inline-block';
  } else {
    document.getElementById('token-title').textContent = 'Programación creada';
    document.getElementById('token-sub').textContent = 'Se ha guardado la acción programada correctamente.';
    document.getElementById('token-box').style.display = 'none';
    document.getElementById('copy-token-btn').style.display = 'none';
  }
  document.getElementById('token-overlay').classList.add('open');
}

document.getElementById('sp-close').addEventListener('click', closeSidePanel);
document.getElementById('sp-cancel').addEventListener('click', closeSidePanel);
document.getElementById('sp-submit').addEventListener('click', submitProgramacion);
document.getElementById('token-close').addEventListener('click', function(){ document.getElementById('token-overlay').classList.remove('open'); });
document.getElementById('copy-token-btn').addEventListener('click', function(){
  var txt = document.getElementById('token-box').textContent;
  navigator.clipboard.writeText(txt).then(function(){
    var btn = document.getElementById('copy-token-btn');
    btn.textContent = 'Copiado ✓';
    setTimeout(function(){ btn.textContent = 'Copiar código'; }, 1500);
  }).catch(function(){});
});

function pageGeneric(){
  return '<div class="page"><div class="page-header">' + enunciadoHtml() + '<div style="font-size:18px;font-weight:600;color:#1a1a1a;">Sección en construcción</div></div></div>';
}

document.getElementById('sidebar-nav').addEventListener('click', function(e){
  var toggleEl = e.target.closest('[data-toggle]');
  var pageEl = e.target.closest('[data-page]');
  if (toggleEl && !pageEl){
    var sub = document.getElementById('sub-' + toggleEl.dataset.toggle);
    sub.classList.toggle('open');
    return;
  }
  if (pageEl){ goPage(pageEl.dataset.page); }
});

goPage('inicio');
</script>
</body>
</html>
