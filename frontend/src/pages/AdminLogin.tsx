import React, { useState } from 'react';
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
  useToast,
  InputGroup,
  InputRightElement,
  IconButton,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import { authAPI } from '../services/api';

const AdminLogin = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Call the login API
      const response = await authAPI.login({
        username: email,
        password: password
      });

      // Store the tokens
      if (response.access) {
        localStorage.setItem('access_token', response.access);
        if (response.refresh) {
          localStorage.setItem('refresh_token', response.refresh);
        }
        // Set admin token for admin-specific routes
        localStorage.setItem('adminToken', response.access);
        
        toast({
          title: 'Login successful',
          description: 'Welcome to the admin dashboard',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
        
        navigate('/admin/dashboard');
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error: any) {
      console.error('Login error:', error);
      toast({
        title: 'Login failed',
        description: error.message || 'Please check your credentials and try again',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.sm" py={10}>
      <VStack spacing={8} as="form" onSubmit={handleSubmit}>
        <Box textAlign="center">
          <Heading size="xl" mb={2}>
            Admin Login
          </Heading>
          <Text color="gray.600">
            Access the admin dashboard to manage products and recommendations
          </Text>
        </Box>

        <FormControl isRequired>
          <FormLabel>Email</FormLabel>
          <Input
            type="email"
            placeholder="admin@skincare.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Password</FormLabel>
          <InputGroup>
            <Input
              type={showPassword ? 'text' : 'password'}
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <InputRightElement>
              <IconButton
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                icon={showPassword ? <ViewOffIcon /> : <ViewIcon />}
                variant="ghost"
                onClick={() => setShowPassword(!showPassword)}
              />
            </InputRightElement>
          </InputGroup>
        </FormControl>

        <Button
          colorScheme="red"
          size="lg"
          w="100%"
          type="submit"
          isLoading={isLoading}
          loadingText="Signing in..."
          className="button-primary"
        >
          Sign In
        </Button>
      </VStack>
    </Container>
  );
};

export default AdminLogin; 