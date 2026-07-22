export type User = { email: string };

export type Pyme = {
  id: number;
  name: string;
  legal_name: string;
  address: string;
  locality: string;
  province: string;
  tax_id: string | null;
  website: string;
  description: string;
  work_type: string;
  enterprise_type: string;
  sector: string;
  maturity_score: string | null;
  maturity_level: number | null;
  maturity_band: string | null;
  rating: number | null;
  latitud: string;
  longitud: string;
};

export type FilterOptions = {
  work_types: string[];
  enterprise_types: string[];
  sectors: string[];
  provinces: string[];
};

export type ChartDatum = { label?: string; count: number; [key: string]: unknown };

export type Summary = {
  total_companies: number;
  distinct_sectors: number;
  average_maturity_score: number | null;
  high_maturity_count: number;
  by_sector: ChartDatum[];
  by_work_type: ChartDatum[];
  by_maturity_band: ChartDatum[];
  by_maturity_level: ChartDatum[];
  companies: Pyme[];
  table: Array<{
    province: string;
    work_type: string;
    enterprise_type: string;
    count: number;
    average_maturity: number | null;
  }>;
};
