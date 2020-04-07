import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { stringify } from 'querystring';
import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/internal/operators';

interface VersionDetails {
  project_name: string;
  project_version: string;
  
}

@Injectable({
  providedIn: 'root'
})

export class ComboApiService {
  readonly server_address = "127.0.0.1"
  readonly port = "9595"

  constructor(private http: HttpClient) { }

  getProjectSource(project_version: string, project_name: string) {
    let get_request_url = `http://${this.server_address}:${this.port}/project/${project_name}/${project_version}`;
    return this.http.get(get_request_url)
  }

  getAvaliableVersions() {
    let get_request_url = `http://${this.server_address}:${this.port}/project`;
    return this.http.get(get_request_url)
  }

  getUploadParams(project_type: string) {
    let get_request_url = `http://${this.server_address}:${this.port}/upload_params/${project_type}`;
    return this.http.get(get_request_url)
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);  
      return of(result as T);
    };
  }

  addProject(project_name: string) : Observable<null> {
    let post_request_url = `http://${this.server_address}:${this.port}/project/${project_name}`;
    
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Authorization': 'my-auth-token'
      })
    }

    return this.http.post(post_request_url, null, httpOptions).pipe(
      catchError(this.handleError('addHero', null))
    );
  }

  addVersion(project_name: string, project_version: string, type_parameters: Map<string, string>) : Observable<Map<string,string>> {
    console.log(type_parameters);
    let post_request_url = `http://${this.server_address}:${this.port}/project/${project_name}/${project_version}`;
    
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'Authorization': 'my-auth-token'
      })
    }

    return this.http.post<Map<string,string>>(post_request_url, type_parameters, httpOptions).pipe(
      catchError(this.handleError('addHero', type_parameters))
    );
  }
}
