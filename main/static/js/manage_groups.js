

manageGroupsInit();
function manageGroupsInit(){
    load_groups(user_id);
}

async function getGroups(teacher_id){
    try {
        const response = await fetchData(`get_groups/${teacher_id}`);
        return response.groups;
    }
    catch (error){
        console.error(error);
        return [];
    }
}

function load_groups(user_id){
    const groups_data = getGroups(user_id);
    console.log(groups_data);
}

function generateGroupElement(group_info, schedules){

}