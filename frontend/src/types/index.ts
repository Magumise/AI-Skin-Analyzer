export interface Product {
  id: number;
  name: string;
  brand: string;
  category: string;
  description: string;
  price: number;
  stock: number;
  image: string;
  suitable_for: string[];
  targets: string[];
  when_to_apply: string[];
}

export interface AnalysisResult {
  conditions: string[];
  recommendations: string[];
  severity: 'mild' | 'moderate' | 'severe';
  confidence: number;
  image_url?: string;
}

export interface User {
  id: number;
  email: string;
  name: string;
  role: 'user' | 'admin';
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface SkinType {
  [key: string]: boolean;
  normal: boolean;
  dry: boolean;
  oily: boolean;
  combination: boolean;
  sensitive: boolean;
}

export interface SkinConcerns {
  [key: string]: boolean;
  acne: boolean;
  wrinkles: boolean;
  darkSpots: boolean;
  redness: boolean;
  dryness: boolean;
  oiliness: boolean;
  sensitivity: boolean;
  aging: boolean;
} 