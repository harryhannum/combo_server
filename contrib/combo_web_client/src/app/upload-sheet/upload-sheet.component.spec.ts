import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadSheetComponent } from './upload-sheet.component';

describe('UploadSheetComponent', () => {
  let component: UploadSheetComponent;
  let fixture: ComponentFixture<UploadSheetComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UploadSheetComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UploadSheetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
