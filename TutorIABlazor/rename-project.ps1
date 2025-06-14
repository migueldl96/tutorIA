param (
    [string]$Path = ".",
    [string]$Old = "TutorIA",
    [string]$New = "TutorIA"
)

Write-Host "?? Ruta base: $Path"
Write-Host "?? Reemplazando '$Old' por '$New' en contenido, nombres de archivos y carpetas..."

# 1?? Reemplazar contenido en archivos
Get-ChildItem -Path $Path -Recurse -File | ForEach-Object {
    try {
        (Get-Content $_.FullName -Raw -ErrorAction Stop) -replace $Old, $New | Set-Content $_.FullName
        Write-Host "? Contenido reemplazado en: $($_.FullName)"
    } catch {
        Write-Warning "?? No se pudo procesar: $($_.FullName)"
    }
}

# 2?? Renombrar archivos
Get-ChildItem -Path $Path -Recurse -File | Where-Object { $_.Name -like "*$Old*" } | ForEach-Object {
    $newName = $_.Name -replace [Regex]::Escape($Old), $New
    $newPath = Join-Path -Path $_.DirectoryName -ChildPath $newName
    Rename-Item -Path $_.FullName -NewName $newPath
    Write-Host "?? Archivo renombrado: $($_.Name) ? $newName"
}

# 3?? Renombrar carpetas (de las más profundas a las superficiales)
Get-ChildItem -Path $Path -Recurse -Directory | Sort-Object FullName -Descending | Where-Object { $_.Name -like "*$Old*" } | ForEach-Object {
    $newName = $_.Name -replace [Regex]::Escape($Old), $New
    $parentPath = Split-Path $_.FullName -Parent
    $newPath = Join-Path -Path $parentPath -ChildPath $newName
    Rename-Item -Path $_.FullName -NewName $newPath
    Write-Host "?? Carpeta renombrada: $($_.FullName) ? $newPath"
}

Write-Host "? Proceso completado con éxito."

