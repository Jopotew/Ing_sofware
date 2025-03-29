from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import FastAPI, Depends, HTTPException, status, Form, UploadFile, File





oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token")








