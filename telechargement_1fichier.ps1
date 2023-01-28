#@author: matth

# dans la contrab : 0 8-22/2,00 * * * pwsh /home/pi/telechargement_1fichier/telechargement_1fichier.ps1 >> /dev/null 2>&1


$cheminTelechargement='/media/pi/cloud/Films/telechargement/'
$cheminScript='/home/pi/telechargement_1fichier/'

#on regarde si le disque dur est connecté avant de lancer le téléchargement
if ( Test-Path -Path $cheminTelechargement -PathType Container ){

    $APIK='cle api'
    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("Authorization", 'Bearer ' + $APIK)

    $fichiers = Invoke-RestMethod -Method Post -Uri "https://api.1fichier.com/v1/file/ls.cgi" -ContentType "application/json" -Headers $headers -Body ( @{ "pretty" = 1; "folder_id" = 0 } |ConvertTo-Json)

    #$fichiers = $fichiers.items
    $nbrFichiers = $fichiers.items.Count

    for ($num = 0 ; $num -le $nbrFichiers-1 ; $num++){
        $url = $fichiers.items[$num].url
        $name = $fichiers.items[$num].filename
        Write-Output $name
        Write-Output $url

        $token = Invoke-RestMethod -Method Post -Uri "https://api.1fichier.com/v1/download/get_token.cgi" -ContentType "application/json" -Headers $headers -Body ( @{ "pretty" = 1; "url" = $url } |ConvertTo-Json)
        Write-Output $token.url

        $retourDl = python3 $cheminScript"dl_fichier.py" $token.url $cheminTelechargement$name
        if($retourDl){
            Write-Output "supression du fichier de la liste"
            Invoke-RestMethod -Method Post -Uri "https://api.1fichier.com/v1/file/rm.cgi" -ContentType "application/json" -Headers $headers -Body ( @{ "pretty" = 1; "files" = @(@{"url"=$url }) } |ConvertTo-Json)
        }else{
            Write-Output "pas de suppressions"
        }

        Write-Output "DL fini"

    }
    
    python3 $cheminScript"rangement.py" $cheminTelechargement
}
