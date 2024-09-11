import axios from "axios";
import sanitize from "sanitize-html";

const axiosInstance = axios.create({
    baseURL: "http://localhost:5000/"
});

export const getSources = async () => {
    const res = await axiosInstance.get("sources");
    
    return res?.data?.sources;
}


export const addSource = async (name, url) => {
    const res = await axiosInstance.post("sources", {
            name: name,
            url: url
        }
    );
    return res;
}

export const delSource = async (id) => {
    const res = await axiosInstance.post("sources/delete", {
        id: id
    }
    );
    return res;
}

export const getStories = async () => {
    const res = await axiosInstance.get("stories/all");
    res?.data?.stories.map((item) => item.summary = sanitize(item.summary));
    return res?.data;
}