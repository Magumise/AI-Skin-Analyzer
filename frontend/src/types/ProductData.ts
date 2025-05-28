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
  suitable_for: string;
  targets: string;
  when_to_apply: string;
}

// Export as both named and default export for better compatibility
export default ProductData;

// Add type declaration for module
declare module '../types/ProductData' {
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
  export default ProductData;
} 