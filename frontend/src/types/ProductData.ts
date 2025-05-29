// Product data interface for the application
export interface ProductData {
  id?: number;
  price: number;
  stock: number;
  name: string;
  brand: string;
  category: string;
  description: string;
  image: string | File;
  suitable_for: string[];
  targets: string[];
  when_to_apply: string[];
  [key: string]: string | number | File | string[] | undefined;
}

// Export as both named and default export for better compatibility
export default ProductData; 