import { TestBed } from '@angular/core/testing';

import { ComboApiService } from './combo-api.service';

describe('ComboApiService', () => {
  let service: ComboApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ComboApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
