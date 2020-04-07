import { Component, OnInit, Inject } from '@angular/core';
import { MatBottomSheetRef, MAT_BOTTOM_SHEET_DATA } from '@angular/material/bottom-sheet';
import { ComboApiService } from '../combo-api.service'

@Component({
  selector: 'app-upload-sheet',
  templateUrl: './upload-sheet.component.html',
  styleUrls: ['./upload-sheet.component.scss']
})
export class UploadSheetComponent implements OnInit {
  constructor(@Inject(MAT_BOTTOM_SHEET_DATA) public data: any, private _comboService: ComboApiService) { }
  
  projectNameValue : string = ""
  existingProjectNameValue : string = ""
  projectVersionValue : string = ""
  selectedVersionType : string = ""
  customUploadParamValue : string = "";

  projectTypes : Array<string> = ["git", "other"]

  projectUploadParams : Map<string, Array<string>> = new Map();
  projectCustomUploadParams : Map<string, Array<string>> = new Map();

  projectUploadParamValues : Map<string, string> = new Map();

  ngOnInit(): void {
    for (let i = 0; i < this.projectTypes.length; i++)
    {
      this._comboService.getUploadParams(this.projectTypes[i]).subscribe(data => {
        this.ParseUploadParams(data, this.projectTypes[i]);
      });

      this.projectCustomUploadParams.set(this.projectTypes[i], new Array());
    }
  }

  ParseUploadParams(data: Object, type: string)
  {
    if (type == null)
    {
      return
    }
 
    let upload_params = (JSON.parse(data.toString()) as Array<string>);

    if (upload_params[0].length == 0)
    {
      upload_params.splice(upload_params?.indexOf(""), 1);
    }

    this.projectUploadParams.set(type, upload_params);
  }

  AddCustomParam(projectType: string, customParam: string)
  {
    if (projectType == "" || customParam == "" || this.projectCustomUploadParams.get(projectType).includes(customParam))
    {
      return;
    }
    
    this.projectCustomUploadParams.get(projectType).push(customParam);
  }

  Upload()
  {
    let isNewProject = (this.projectNameValue != "");
    if (isNewProject)
    {
      this._comboService.addProject(this.projectNameValue).subscribe( data=> {
        console.log(data);
      });
    }

    if (this.projectVersionValue != "")
    {
      this.projectUploadParamValues["type"] = this.selectedVersionType;
      this._comboService.addVersion(this.projectNameValue != ""?this.projectNameValue:this.existingProjectNameValue,
       this.projectVersionValue, this.projectUploadParamValues).subscribe( data=> {
        console.log(data);
      });
    }

  }
}
