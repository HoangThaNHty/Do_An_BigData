# Native Windows Office export fallback. Uses a separate application instance.
param([switch]$ReportOnly,[switch]$SlidesOnly)
$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path $PSScriptRoot -Parent
$Build=Join-Path $ProjectRoot 'artifacts/document_build'
$Output=Join-Path $ProjectRoot 'deliverables'
$Content=Get-Content -LiteralPath "$Build/content.json" -Raw -Encoding UTF8 | ConvertFrom-Json
New-Item -ItemType Directory -Force -Path "$Build/report_pages","$Build/slides" | Out-Null
if(-not $SlidesOnly){
    $Word=New-Object -ComObject Word.Application
    $Word.Visible=$false; $Word.DisplayAlerts=0
    $Doc=$null
    try {
        $Doc=$Word.Documents.Open("$Build/report.html",$false,$false)
        $Doc.PageSetup.PaperSize=7 # A4
        $Doc.PageSetup.TopMargin=56.7;$Doc.PageSetup.BottomMargin=56.7
        $Doc.PageSetup.LeftMargin=70.9;$Doc.PageSetup.RightMargin=56.7
        $Doc.Styles.Item(-1).Font.Name='Times New Roman';$Doc.Styles.Item(-1).Font.Size=13
        $Doc.Styles.Item(-1).Font.Color=0
        $Doc.Styles.Item(-2).Font.Name='Times New Roman';$Doc.Styles.Item(-2).Font.Size=16
        $Doc.Styles.Item(-2).Font.Color=0;$Doc.Styles.Item(-2).ParagraphFormat.KeepWithNext=-1
        $ImageRange=$Doc.Content.Duplicate;$ImageRange.Find.Text='__FIGURE_1__'
        if($ImageRange.Find.Execute()){
            $ImageRange.Text=''
            $Image=$Doc.InlineShapes.AddPicture("$ProjectRoot/artifacts/verification/web/01-overview.png",$false,$true,$ImageRange)
            $Image.LockAspectRatio=-1;$Image.Width=420
        }
        # Import HTML heading text into native heading styles for the editable TOC.
        $Headings=@($Content.sections | ForEach-Object {$_.title})
        foreach($Paragraph in $Doc.Paragraphs){
            $Text=$Paragraph.Range.Text.Trim([char]13,[char]7)
            if($Headings -contains $Text){$Paragraph.Range.Style=$Doc.Styles.Item(-2);$Paragraph.Range.ParagraphFormat.PageBreakBefore=-1}
            if($Text -eq 'Mục lục'){$Paragraph.Range.Style=$Doc.Styles.Item(-1);$Paragraph.Range.Font.Bold=-1;$Paragraph.Range.Font.Size=16;$Paragraph.Range.ParagraphFormat.PageBreakBefore=-1;$Paragraph.Range.ParagraphFormat.OutlineLevel=10}
            if($Text -eq $Content.title){$Paragraph.Range.Style=$Doc.Styles.Item(-63);$Paragraph.Range.Font.Color=0}
            if($Text.Contains('SHA256') -or $Text.Contains('commit ') -or $Text.Contains('https://') -or $Text.Contains('_')){$Paragraph.Range.ParagraphFormat.Alignment=0}
        }
        $TocRange=$Doc.Content.Duplicate
        $TocRange.Find.Text='__TOC__'
        if($TocRange.Find.Execute()) {
            $TocRange.Text=''
            $null=$Doc.TablesOfContents.Add($TocRange,$true,1,1,$false,'',$true,$true)
        }
        foreach($Table in $Doc.Tables){
            $Table.Rows.AllowBreakAcrossPages=0;$Table.Rows.Item(1).HeadingFormat=-1
            $Table.Range.Font.Name='Times New Roman';$Table.Range.Font.Size=10.5
            $Table.Range.ParagraphFormat.SpaceAfter=3;$Table.Range.ParagraphFormat.SpaceBefore=3
        }
        $Doc.Sections.Item(1).PageSetup.DifferentFirstPageHeaderFooter=-1
        $Footer=$Doc.Sections.Item(1).Footers.Item(1).Range
        $Footer.Font.Name='Times New Roman';$Footer.Font.Size=10;$Footer.Font.Color=0
        $Footer.ParagraphFormat.Alignment=1
        $null=$Footer.Fields.Add($Footer,33) # PAGE
        $Doc.Repaginate();foreach($Toc in $Doc.TablesOfContents){$Toc.Update()}
        $Doc.SaveAs2("$Output/BAO_CAO_DO_AN_NHOM18.docx",16)
        $Doc.ExportAsFixedFormat("$Build/report.pdf",17)
        Write-Output ('Word pages: '+$Doc.ComputeStatistics(2))
    } finally {
        if($Doc){$Doc.Close(0)};$Word.Quit()
        [Runtime.InteropServices.Marshal]::ReleaseComObject($Word) | Out-Null
    }
}
if(-not $ReportOnly){
    $PowerPoint=New-Object -ComObject PowerPoint.Application
    $Presentation=$null
    try {
        $Presentation=$PowerPoint.Presentations.Add(0)
        $Presentation.PageSetup.SlideWidth=960;$Presentation.PageSetup.SlideHeight=540
        function Add-Text($Slide,[string]$Text,[single]$Left,[single]$Top,[single]$Width,[single]$Height,[single]$Size,[int]$Color,[bool]$Bold=$false) {
            $Shape=$Slide.Shapes.AddTextbox(1,$Left,$Top,$Width,$Height)
            $Shape.TextFrame.WordWrap=-1;$Shape.TextFrame.AutoSize=0
            $Shape.TextFrame.MarginLeft=0;$Shape.TextFrame.MarginRight=0
            $Shape.TextFrame.MarginTop=0;$Shape.TextFrame.MarginBottom=0
            $Range=$Shape.TextFrame.TextRange;$Range.Text=$Text
            $Range.Font.Name='Arial';$Range.Font.Size=$Size;$Range.Font.Color.RGB=$Color
            $Range.Font.Bold=if($Bold){-1}else{0}
            $Range.ParagraphFormat.SpaceAfter=if($Size -le 11){0}else{8}
            $Shape.TextFrame2.AutoSize=0
            $Shape.Width=$Width;$Shape.Height=$Height
            return $Shape
        }
        $Ink=0x2F3924;$Green=0x556B16;$Muted=0x737D73
        $Index=0;$Fits=@()
        foreach($Definition in $Content.slides){
            $Index++;$Slide=$Presentation.Slides.Add($Index,12)
            $Slide.FollowMasterBackground=0;$Slide.Background.Fill.ForeColor.RGB=0xFFFFFF
            $null=Add-Text $Slide $Definition.title 54 36 850 83 $(if($Index -eq 1){42}else{32}) $Green $true
            if($Definition.body){$null=Add-Text $Slide $Definition.body 56 142 848 332 23 $Ink}
            if($Definition.table){
                $Rows=$Definition.table.Count;$Columns=$Definition.table[0].Count
                $TableShape=$Slide.Shapes.AddTable($Rows,$Columns,55,146,850,292)
                $Table=$TableShape.Table
                for($Row=1;$Row -le $Rows;$Row++){
                    for($Col=1;$Col -le $Columns;$Col++){
                        $Cell=$Table.Cell($Row,$Col)
                        $Cell.Shape.TextFrame.MarginLeft=12;$Cell.Shape.TextFrame.MarginRight=10
                        $Cell.Shape.TextFrame.MarginTop=8;$Cell.Shape.TextFrame.MarginBottom=8
                        $Cell.Shape.TextFrame.VerticalAnchor=3
                        $Cell.Shape.TextFrame.TextRange.Text=[string]$Definition.table[$Row-1][$Col-1]
                        $Cell.Shape.TextFrame.TextRange.Font.Name='Arial'
                        $Cell.Shape.TextFrame.TextRange.Font.Size=21
                        $Cell.Shape.TextFrame.TextRange.Font.Color.RGB=$Ink
                        $Cell.Shape.TextFrame.TextRange.Font.Bold=if($Row -eq 1){-1}else{0}
                        $Cell.Shape.Fill.ForeColor.RGB=if($Row -eq 1){0xE7F0E9}elseif($Row % 2 -eq 0){0xFAFCFA}else{0xFFFFFF}
                        for($Border=1;$Border -le 4;$Border++){$Cell.Borders.Item($Border).ForeColor.RGB=0xD9D9D9;$Cell.Borders.Item($Border).Weight=.5}
                    }
                }
            }
            if($Definition.image){
                $Picture=$Slide.Shapes.AddPicture((Join-Path $ProjectRoot $Definition.image),0,-1,0,0,-1,-1)
                $Picture.LockAspectRatio=-1
                if($Picture.Width/$Picture.Height -gt 850/365){$Picture.Width=850}else{$Picture.Height=365}
                $Picture.Left=(960-$Picture.Width)/2;$Picture.Top=130
            }
            if($Definition.footer){$null=Add-Text $Slide $Definition.footer 55 458 845 44 17 $Muted}
            $null=Add-Text $Slide ([string]$Index) 880 511 26 19 11 $Muted
            $Slide.NotesPage.Shapes.Placeholders.Item(2).TextFrame.TextRange.Text=$Definition.notes
            foreach($Shape in $Slide.Shapes){
                if($Shape.HasTextFrame -eq -1 -and $Shape.TextFrame.HasText -eq -1){
                    $Height=$Shape.TextFrame.TextRange.BoundHeight
                    $Fits+=@{slide=$Index;text=$Shape.TextFrame.TextRange.Text;bound_height=$Height;box_height=$Shape.Height}
                    if($Height -gt $Shape.Height+2){throw "Text overflow on slide ${Index}: $($Shape.TextFrame.TextRange.Text) ($Height > $($Shape.Height))"}
                }
            }
            $Slide.Export("$Build/slides/slide-$Index.png",'PNG',1600,900)
        }
        $Presentation.SaveAs("$Output/THUYET_TRINH_DO_AN_NHOM18.pptx",24)
        $Fits | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath "$Build/slide_text_fit.json" -Encoding UTF8
        Write-Output ('PowerPoint slides: '+$Presentation.Slides.Count)
    } finally {
        if($Presentation){$Presentation.Close()};$PowerPoint.Quit()
        [Runtime.InteropServices.Marshal]::ReleaseComObject($PowerPoint) | Out-Null
    }
}
