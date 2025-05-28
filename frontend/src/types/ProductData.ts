export interface ProductData {
  id?: number;
  price: number;
  stock: number;
  name: string;
  brand: string;
  category: string;
  description: string;
  image: string | File;
  suitable_for: string;
  targets: string;
  when_to_apply: string;
} 