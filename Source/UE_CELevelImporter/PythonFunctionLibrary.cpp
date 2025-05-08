// Fill out your copyright notice in the Description page of Project Settings.


#include "PythonFunctionLibrary.h"
#include "WorldPartition/DataLayer/DataLayerUtils.h"


bool UPythonFunctionLibrary::SetDataLayerShortName(UDataLayerInstance* InDataLayerInstance, const FString& InNewShortName) {
	return FDataLayerUtils::SetDataLayerShortName(InDataLayerInstance, InNewShortName);
}