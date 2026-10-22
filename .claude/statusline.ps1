# Ligne de statut Claude Code : remplissage du contexte en vert / orange / rouge.
# Vert < 50 % (on continue), orange 50–80 % (penser à /compact), rouge > 80 % (/compact ou /clear maintenant).
# Lit le JSON envoyé par Claude Code sur l'entrée standard ; à défaut de pourcentage fourni, relit le dernier
# « usage » du transcript (tokens d'entrée + cache) et le rapporte à la taille de la fenêtre.
$ErrorActionPreference = 'SilentlyContinue'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$in = [Console]::In.ReadToEnd() | ConvertFrom-Json

$model = $in.model.display_name
$size = 200000
if ($in.context_window.context_window_size) { $size = [double]$in.context_window.context_window_size }

$used = $null
if ($in.context_window.current_usage) {
  $u = $in.context_window.current_usage
  $used = [double]$u.input_tokens + [double]$u.cache_read_input_tokens + [double]$u.cache_creation_input_tokens
}
if (-not $used -and $in.transcript_path -and (Test-Path $in.transcript_path)) {
  $lines = Get-Content $in.transcript_path -Tail 200
  [array]::Reverse($lines)
  foreach ($l in $lines) {
    if ($l -notmatch '"usage"') { continue }
    $u = ($l | ConvertFrom-Json).message.usage
    if ($u) {
      $used = [double]$u.input_tokens + [double]$u.cache_read_input_tokens + [double]$u.cache_creation_input_tokens
      break
    }
  }
}

$e = [char]27
if ($used) {
  $pct = [math]::Round(100 * $used / $size)
  if ($pct -lt 50) { $c = "$e[32m"; $tip = 'ok' }
  elseif ($pct -lt 80) { $c = "$e[33m"; $tip = '/compact bientôt' }
  else { $c = "$e[31m"; $tip = '/compact ou /clear' }
  $k = [math]::Round($used / 1000)
  $ctx = "$c● $pct % ($k k / $([math]::Round($size / 1000)) k) — $tip$e[0m"
} else {
  $ctx = "$e[32m● 0 %$e[0m"
}

$cost = ''
if ($in.cost.total_cost_usd) { $cost = ' | ' + ('{0:N2} $' -f [double]$in.cost.total_cost_usd) }
Write-Output "$model | $ctx$cost"
