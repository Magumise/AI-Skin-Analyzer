import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  VStack,
  Heading,
  Text,
  FormControl,
  FormLabel,
  Input,
  Button,
  HStack,
  Divider,
  useToast,
  InputGroup,
  InputRightElement,
  IconButton,
  Select,
  Checkbox,
  SimpleGrid,
  useColorModeValue,
  ScaleFade,
  Flex,
  Image,
  Stack,
  Tooltip,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon, InfoIcon } from '@chakra-ui/icons';
import { motion } from 'framer-motion';
import bgImage from '../new.png';  // Make sure this path matches your image location
import { authAPI } from '../services/api';
import APITest from '../components/APITest';

const MotionBox = motion(Box);

interface SkinType {
  dry: boolean;
  oily: boolean;
  combination: boolean;
  normal: boolean;
  sensitive: boolean;
}

interface SkinConcerns {
  acne: boolean;
  aging: boolean;
  pigmentation: boolean;
  redness: boolean;
  dullness: boolean;
  wrinkles: boolean;
  darkSpots: boolean;
  dryness: boolean;
  oiliness: boolean;
  sensitivity: boolean;
}

interface FormData {
  firstName: string;
  lastName: string;
  email: string;
  age: string;
  sex: string;
  country: string;
  password: string;
  confirmPassword: string;
  skinType: SkinType;
  skinConcerns: SkinConcerns;
}

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();
  
  // Theme colors
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  const [formData, setFormData] = useState<FormData>({
    firstName: '',
    lastName: '',
    email: '',
    age: '',
    sex: '',
    country: '',
    password: '',
    confirmPassword: '',
    skinType: {
      dry: false,
      oily: false,
      combination: false,
      normal: false,
      sensitive: false
    },
    skinConcerns: {
      acne: false,
      aging: false,
      pigmentation: false,
      redness: false,
      dullness: false,
      wrinkles: false,
      darkSpots: false,
      dryness: false,
      oiliness: false,
      sensitivity: false
    }
  });

  const [imagePath, setImagePath] = useState('');
  const [imageError, setImageError] = useState(false);

  const skinTypes: (keyof SkinType)[] = ['normal', 'dry', 'oily', 'combination', 'sensitive'];
  const skinConcerns: (keyof SkinConcerns)[] = ['acne', 'wrinkles', 'darkSpots', 'redness', 'dryness', 'oiliness', 'sensitivity', 'aging', 'pigmentation', 'dullness'];

  useEffect(() => {
    // Try to get the correct image path
    try {
      const imageUrl = new URL('../new.png', import.meta.url).href;
      setImagePath(imageUrl);
      console.log('Image URL:', imageUrl); // For debugging
    } catch (error) {
      console.error('Error creating image URL:', error);
    }
  }, []);

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      try {
        const isValid = await authAPI.verifyToken();
        if (isValid) {
          navigate('/skin-analysis');
        }
      } catch (error) {
        console.error('Auth check error:', error);
      }
    };
    checkAuth();
  }, [navigate]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSkinTypeChange = (type: keyof SkinType, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      skinType: {
        ...prev.skinType,
        [type]: checked
      }
    }));
  };

  const handleSkinConcernChange = (concern: keyof SkinConcerns, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      skinConcerns: {
        ...prev.skinConcerns,
        [concern]: checked
      }
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      if (!isLogin) {
        // Registration validation
        if (formData.password !== formData.confirmPassword) {
          toast({
            title: 'Passwords do not match',
            status: 'error',
            duration: 3000,
            isClosable: true,
          });
          return;
        }

        // Validate password strength
        if (formData.password.length < 8) {
          toast({
            title: 'Password too weak',
            description: 'Password must be at least 8 characters long',
            status: 'error',
            duration: 3000,
            isClosable: true,
          });
          return;
        }

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email)) {
          toast({
            title: 'Invalid email format',
            status: 'error',
            duration: 3000,
            isClosable: true,
          });
          return;
        }

        // Validate required fields
        if (!formData.email || !formData.password || !formData.firstName || !formData.lastName) {
          toast({
            title: 'Missing required fields',
            description: 'Please fill in all required fields',
            status: 'error',
            duration: 3000,
            isClosable: true,
          });
          return;
        }

        // Format the data for the backend
        const registrationData = {
          email: formData.email,
          password: formData.password,
          first_name: formData.firstName,
          last_name: formData.lastName,
          username: formData.email.split('@')[0], // Generate username from email
          age: formData.age ? parseInt(formData.age) : null,
          sex: formData.sex || null,
          country: formData.country || null,
          skin_type: Object.entries(formData.skinType)
            .filter(([_, value]) => value)
            .map(([key]) => key),
          skin_concerns: Object.entries(formData.skinConcerns)
            .filter(([_, value]) => value)
            .map(([key]) => key)
        };

        console.log('Sending registration data:', registrationData);

        const response = await authAPI.register(registrationData);
        console.log('Registration successful:', response.data);
        
        toast({
          title: 'Account created successfully!',
          description: 'Welcome to AI Skin Analyzer',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });

        navigate('/skin-analysis');
      } else {
        // Login
        const response = await authAPI.login({
          email: formData.email,
          password: formData.password
        });

        console.log('Login successful:', response.data);

        toast({
          title: 'Login successful!',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });

        navigate('/skin-analysis');
      }
    } catch (error: any) {
      console.error(isLogin ? 'Login error:' : 'Registration error:', error);
      let errorMessage = isLogin ? 'Login failed. Please check your credentials.' : 'Registration failed. Please try again.';
      
      if (error.response?.data) {
        if (typeof error.response.data === 'object') {
          const errors = Object.entries(error.response.data)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join('\n');
          errorMessage = errors;
        } else {
          errorMessage = error.response.data.detail || error.response.data.message || errorMessage;
        }
      } else if (error.message) {
        errorMessage = error.message;
      }

      toast({
        title: isLogin ? 'Login failed' : 'Registration failed',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box
      minH="100vh"
      bgGradient="linear(to-r, pink.50, white)"
      py={8}
    >
      <Container maxW="7xl">
        <Box
          bg="white"
          borderRadius="3xl"
          overflow="hidden"
          boxShadow="2xl"
          mx="auto"
        >
          <Flex direction={{ base: 'column', lg: 'row' }}>
            {/* Left side - Form */}
            <Box 
              flex={1}
              p={8}
              borderRight="1px"
              borderColor="pink.100"
            >
              <VStack
                as="form"
                onSubmit={handleSubmit}
                spacing={6}
                align="stretch"
                w="full"
                maxW="500px"
                mx="auto"
              >
                <MotionBox
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  textAlign="center"
                >
                  <Heading 
                    fontSize="3xl"
                    bgGradient="linear(to-r, pink.400, purple.500)"
                    bgClip="text"
                    letterSpacing="tight"
                    mb={2}
                  >
                    {isLogin ? 'Welcome Back' : 'Begin Your Skin Journey'}
                  </Heading>
                  <Text color="gray.600" fontSize="lg">
                    {isLogin
                      ? 'Sign in to continue your personalized skin care experience'
                      : 'Create your account for personalized skin analysis'}
                  </Text>
                </MotionBox>

                {!isLogin && (
                  <SimpleGrid columns={{ base: 1, sm: 2 }} spacing={6}>
                    <FormControl isRequired>
                      <FormLabel fontWeight="medium">First Name</FormLabel>
                      <Input
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleInputChange}
                        placeholder="John"
                        size="lg"
                        bg="gray.50"
                        border="2px"
                        borderColor="gray.200"
                        _hover={{ borderColor: 'pink.200' }}
                        _focus={{ borderColor: 'pink.400', boxShadow: '0 0 0 1px pink.400' }}
                        transition="all 0.2s"
                      />
                    </FormControl>
                    <FormControl isRequired>
                      <FormLabel fontWeight="medium">Last Name</FormLabel>
                      <Input
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleInputChange}
                        placeholder="Doe"
                        size="lg"
                        bg="gray.50"
                        border="2px"
                        borderColor="gray.200"
                        _hover={{ borderColor: 'pink.200' }}
                        _focus={{ borderColor: 'pink.400', boxShadow: '0 0 0 1px pink.400' }}
                        transition="all 0.2s"
                      />
                    </FormControl>
                  </SimpleGrid>
                )}

                <FormControl isRequired>
                  <FormLabel fontWeight="medium">Email</FormLabel>
                  <Input
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="john@example.com"
                    size="lg"
                    bg="gray.50"
                    border="2px"
                    borderColor="gray.200"
                    _hover={{ borderColor: 'pink.200' }}
                    _focus={{ borderColor: 'pink.400', boxShadow: '0 0 0 1px pink.400' }}
                    transition="all 0.2s"
                  />
                </FormControl>

                {!isLogin && (
                  <>
                    <SimpleGrid columns={{ base: 1, sm: 2 }} spacing={6}>
                      <FormControl isRequired>
                        <FormLabel fontWeight="medium">Age</FormLabel>
                        <Input
                          name="age"
                          type="number"
                          value={formData.age}
                          onChange={handleInputChange}
                          placeholder="25"
                          size="lg"
                          bg="gray.50"
                          border="2px"
                          borderColor="gray.200"
                          _hover={{ borderColor: 'pink.200' }}
                          _focus={{ borderColor: 'pink.400', boxShadow: '0 0 0 1px pink.400' }}
                          transition="all 0.2s"
                        />
                      </FormControl>
                      <FormControl isRequired>
                        <FormLabel fontWeight="medium">Sex</FormLabel>
                        <Select
                          name="sex"
                          value={formData.sex}
                          onChange={handleInputChange}
                          placeholder="Select gender"
                          size="lg"
                          bg="gray.50"
                          border="2px"
                          borderColor="gray.200"
                          _hover={{ borderColor: 'pink.200' }}
                          _focus={{ borderColor: 'pink.400', boxShadow: '0 0 0 1px pink.400' }}
                          transition="all 0.2s"
                        >
                          <option value="male">Male</option>
                          <option value="female">Female</option>
                          <option value="other">Other</option>
                        </Select>
                      </FormControl>
                    </SimpleGrid>

                    <FormControl isRequired>
                      <FormLabel fontWeight="medium">Country</FormLabel>
                      <Select
                        name="country"
                        value={formData.country}
                        onChange={handleInputChange}
                        placeholder="Select country"
                        size="lg"
                        bg="gray.50"
                        border="2px"
                        borderColor="gray.200"
                        _hover={{ borderColor: 'pink.200' }}
                        _focus={{ borderColor: 'pink.400', boxShadow: '0 0 0 1px pink.400' }}
                        transition="all 0.2s"
                      >
                        <option value="MY">Malaysia</option>
                        <option value="SG">Singapore</option>
                        <option value="US">United States</option>
                        <option value="UK">United Kingdom</option>
                        <option value="AU">Australia</option>
                      </Select>
                    </FormControl>

                    <Box
                      bg="gray.50"
                      p={6}
                      borderRadius="xl"
                      border="2px"
                      borderColor="pink.100"
                    >
                      <Text
                        fontSize="lg"
                        fontWeight="bold"
                        color="pink.600"
                        mb={4}
                      >
                        Skin Profile
                      </Text>
                      <SimpleGrid columns={2} spacing={6}>
                        <FormControl>
                          <FormLabel fontWeight="medium" color="gray.700">
                            Skin Type
                          </FormLabel>
                          <VStack align="start" spacing={3}>
                            {skinTypes.map((type) => (
                              <Checkbox
                                key={type}
                                isChecked={formData.skinType[type]}
                                onChange={(e) => handleSkinTypeChange(type, e.target.checked)}
                              >
                                {type.charAt(0).toUpperCase() + type.slice(1)}
                              </Checkbox>
                            ))}
                          </VStack>
                        </FormControl>
                        <FormControl>
                          <FormLabel fontWeight="medium" color="gray.700">
                            Skin Concerns
                          </FormLabel>
                          <VStack align="start" spacing={3}>
                            {skinConcerns.map((concern) => (
                              <Checkbox
                                key={concern}
                                isChecked={formData.skinConcerns[concern]}
                                onChange={(e) => handleSkinConcernChange(concern, e.target.checked)}
                              >
                                {concern.replace(/([A-Z])/g, ' $1').trim()}
                              </Checkbox>
                            ))}
                          </VStack>
                        </FormControl>
                      </SimpleGrid>
                    </Box>
                  </>
                )}

                <FormControl isRequired>
                  <FormLabel fontWeight="medium">Password</FormLabel>
                  <InputGroup size="lg">
                    <Input
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      value={formData.password}
                      onChange={handleInputChange}
                      placeholder="Enter your password"
                      bg="gray.50"
                      border="2px"
                      borderColor="gray.200"
                      _hover={{ borderColor: 'pink.200' }}
                      _focus={{ borderColor: 'pink.400', boxShadow: '0 0 0 1px pink.400' }}
                      transition="all 0.2s"
                    />
                    <InputRightElement width="4.5rem">
                      <IconButton
                        h="1.75rem"
                        size="sm"
                        aria-label={showPassword ? 'Hide password' : 'Show password'}
                        icon={showPassword ? <ViewOffIcon /> : <ViewIcon />}
                        variant="ghost"
                        colorScheme="pink"
                        onClick={() => setShowPassword(!showPassword)}
                      />
                    </InputRightElement>
                  </InputGroup>
                </FormControl>

                {!isLogin && (
                  <FormControl isRequired>
                    <FormLabel fontWeight="medium">Confirm Password</FormLabel>
                    <InputGroup size="lg">
                      <Input
                        name="confirmPassword"
                        type={showConfirmPassword ? 'text' : 'password'}
                        value={formData.confirmPassword}
                        onChange={handleInputChange}
                        placeholder="Confirm your password"
                        bg="gray.50"
                        border="2px"
                        borderColor="gray.200"
                        _hover={{ borderColor: 'pink.200' }}
                        _focus={{ borderColor: 'pink.400', boxShadow: '0 0 0 1px pink.400' }}
                        transition="all 0.2s"
                      />
                      <InputRightElement width="4.5rem">
                        <IconButton
                          h="1.75rem"
                          size="sm"
                          aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                          icon={showConfirmPassword ? <ViewOffIcon /> : <ViewIcon />}
                          variant="ghost"
                          colorScheme="pink"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        />
                      </InputRightElement>
                    </InputGroup>
                  </FormControl>
                )}

                <Button
                  type="submit"
                  size="lg"
                  fontSize="md"
                  bgGradient="linear(to-r, pink.400, purple.500)"
                  color="white"
                  _hover={{
                    bgGradient: "linear(to-r, pink.500, purple.600)",
                    transform: "translateY(-2px)",
                    boxShadow: "xl"
                  }}
                  _active={{
                    bgGradient: "linear(to-r, pink.600, purple.700)"
                  }}
                  transition="all 0.2s"
                  isLoading={isLoading}
                >
                  {isLogin ? 'Sign In' : 'Create Account'}
                </Button>

                <HStack justify="center" spacing={2}>
                  <Text color="gray.600">
                    {isLogin ? "Don't have an account?" : 'Already have an account?'}
                  </Text>
                  <Button
                    variant="link"
                    color="pink.500"
                    _hover={{ color: 'pink.600' }}
                    onClick={() => setIsLogin(!isLogin)}
                  >
                    {isLogin ? 'Sign Up' : 'Sign In'}
                  </Button>
                </HStack>
              </VStack>
            </Box>

            {/* Right side - Image */}
            <Box 
              flex={1}
              position="relative"
              display={{ base: 'none', lg: 'block' }}
              bg="pink.50"
              minH="100%"
            >
              <Box
                position="absolute"
                top={0}
                right={0}
                bottom={0}
                left={0}
                bgImage="url('../new.png')"
                bgSize="cover"
                bgPosition="center"
              />
              <Box
                position="absolute"
                top={0}
                right={0}
                bottom={0}
                left={0}
                bg="linear-gradient(45deg, rgba(255,182,193,0.3), rgba(159,122,234,0.3))"
                backdropFilter="blur(1px)"
              />
              <VStack
                position="absolute"
                bottom={10}
                left={0}
                right={0}
                spacing={4}
                p={6}
              >
                <Box
                  bg="rgba(255, 255, 255, 0.9)"
                  p={6}
                  borderRadius="xl"
                  boxShadow="xl"
                  backdropFilter="blur(10px)"
                  maxW="80%"
                  mx="auto"
                >
                  <Heading
                    size="lg"
                    color="pink.500"
                    textAlign="center"
                    mb={2}
                  >
                    AI-Powered Skin Analysis
                  </Heading>
                  <Text
                    color="gray.600"
                    textAlign="center"
                    fontSize="md"
                  >
                    Get personalized skincare recommendations based on advanced AI technology
                  </Text>
                </Box>
              </VStack>
            </Box>
          </Flex>
        </Box>
      </Container>
      
      {/* Add the API Test component */}
      {process.env.NODE_ENV === 'development' && (
        <div className="mt-8">
          <APITest />
        </div>
      )}
    </Box>
  );
};

export default Auth; 