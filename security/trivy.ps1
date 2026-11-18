# Escanea con Trivy las imágenes del compose (HIGH y CRITICAL con arreglo disponible).
# Uso, desde la carpeta del repo API:  .\security\trivy.ps1
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path security/reports | Out-Null
$images = docker compose config --images | Sort-Object -Unique
foreach ($img in $images) {
    $name = ($img -replace '[:/]', '_')
    Write-Host "== $img ==" -ForegroundColor Cyan
    docker run --rm `
        -v //var/run/docker.sock:/var/run/docker.sock `
        -v "${PWD}:/src" -w /src `
        aquasec/trivy:latest image --scanners vuln --severity HIGH,CRITICAL --ignore-unfixed `
        --format table -o "/src/security/reports/trivy_$name.txt" $img
    # Resumen legible: solo las líneas con CVE y los totales (el detalle completo queda en el .txt)
    Select-String -Path "security/reports/trivy_$name.txt" -Pattern "Total:|CVE-" | ForEach-Object { $_.Line.Trim() } | Select-Object -First 25
}
