import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Heading,
  Text,
  VStack,
  HStack,
  Button,
  useColorModeValue,
  Icon,
  SimpleGrid,
  Card,
  CardBody,
  CardHeader,
} from '@chakra-ui/react';
import { FaCamera, FaRobot, FaUserMd, FaShoppingBag } from 'react-icons/fa';
import './HowItWorks.css';
import Navigation from '../components/Navigation';

const HowItWorks = () => {
  const navigate = useNavigate();
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const handleStartAnalysis = () => {
    navigate('/analysis');
  };

  return (
    <Box className="app-container">
      <Navigation />

      {/* Main Content */}
      <Box className="main-content" py={16}>
        <Container maxW="container.xl">
          <VStack spacing={12}>
            <Box textAlign="center">
              <Heading size="2xl" mb={4}>How It Works</Heading>
              <Text fontSize="xl" color="gray.600" maxW="800px" mx="auto">
                Discover your true beauty with our revolutionary AI-powered skin analysis
              </Text>
            </Box>

            <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={8} width="100%">
              {/* Step 1: Upload or Take Photo */}
              <Card 
                borderRadius="xl" 
                overflow="hidden" 
                boxShadow="lg"
                bg={cardBg}
                borderColor={borderColor}
                transition="transform 0.3s"
                _hover={{ transform: 'translateY(-5px)' }}
              >
                <CardHeader bg="red.50">
                  <Flex justify="center" align="center" h="60px">
                    <Icon as={FaCamera} w={8} h={8} color="red.500" />
                  </Flex>
                </CardHeader>
                <CardBody>
                  <VStack spacing={3} align="center" textAlign="center">
                    <Heading size="md">Step 1: Upload or Take Photo</Heading>
                    <Text color="gray.600">
                      Upload a photo of your skin or take a picture using your device's camera
                    </Text>
                  </VStack>
                </CardBody>
              </Card>

              {/* Step 2: AI Analysis */}
              <Card 
                borderRadius="xl" 
                overflow="hidden" 
                boxShadow="lg"
                bg={cardBg}
                borderColor={borderColor}
                transition="transform 0.3s"
                _hover={{ transform: 'translateY(-5px)' }}
              >
                <CardHeader bg="red.50">
                  <Flex justify="center" align="center" h="60px">
                    <Icon as={FaChartBar} w={8} h={8} color="red.500" />
                  </Flex>
                </CardHeader>
                <CardBody>
                  <VStack spacing={3} align="center" textAlign="center">
                    <Heading size="md">Step 2: AI Analysis</Heading>
                    <Text color="gray.600">
                      Our advanced AI analyzes your skin condition with high precision
                    </Text>
                  </VStack>
                </CardBody>
              </Card>

              {/* Step 3: View Results */}
              <Card 
                borderRadius="xl" 
                overflow="hidden" 
                boxShadow="lg"
                bg={cardBg}
                borderColor={borderColor}
                transition="transform 0.3s"
                _hover={{ transform: 'translateY(-5px)' }}
              >
                <CardHeader bg="red.50">
                  <Flex justify="center" align="center" h="60px">
                    <Icon as={FaUpload} w={8} h={8} color="red.500" />
                  </Flex>
                </CardHeader>
                <CardBody>
                  <VStack spacing={3} align="center" textAlign="center">
                    <Heading size="md">Step 3: View Results</Heading>
                    <Text color="gray.600">
                      Get detailed analysis of your skin condition and recommendations
                    </Text>
                  </VStack>
                </CardBody>
              </Card>

              {/* Step 4: Get Products */}
              <Card 
                borderRadius="xl" 
                overflow="hidden" 
                boxShadow="lg"
                bg={cardBg}
                borderColor={borderColor}
                transition="transform 0.3s"
                _hover={{ transform: 'translateY(-5px)' }}
              >
                <CardHeader bg="red.50">
                  <Flex justify="center" align="center" h="60px">
                    <Icon as={FaShoppingCart} w={8} h={8} color="red.500" />
                  </Flex>
                </CardHeader>
                <CardBody>
                  <VStack spacing={3} align="center" textAlign="center">
                    <Heading size="md">Step 4: Get Products</Heading>
                    <Text color="gray.600">
                      Purchase recommended products tailored to your skin needs
                    </Text>
                  </VStack>
                </CardBody>
              </Card>
            </SimpleGrid>

            <Box textAlign="center" mt={8}>
              <Button
                colorScheme="red"
                size="lg"
                onClick={handleStartAnalysis}
                rightIcon={<Icon as={FaArrowRight} />}
              >
                Start Free Analysis
              </Button>
            </Box>
          </VStack>
        </Container>
      </Box>
    </Box>
  );
};

export default HowItWorks; 